import boto3
import requests
import time
import json
import subprocess
from datetime import datetime, timezone
import os
import croniter
import shutil

hass_options = json.load(open('/data/options.json'))
log = lambda value: subprocess.run(f'echo "{datetime.now().strftime("%m/%d/%Y, %H:%M:%S")} | {str(value)}"', shell=True) if hass_options['logging'] else lambda: None
s3 = boto3.client('s3', aws_access_key_id = hass_options['access_key_id'], aws_secret_access_key = hass_options['secret_access_key'])

def encrypt_with_pgp():
    shutil.copyfile(hass_options["pgp_public_key_path"], "public.key")
    # subprocess.run("gpg --import public.key", shell=True)
    # res = subprocess.Popen(["gpg", "--import", "public.key"], stdout=subprocess.PIPE)
    #res = subprocess.run("gpg --import public.key", shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
    # log("TESTING: " + str(res.communicate()))
    subprocess.run("gpg --import public.key", shell=True, stdout=subprocess.PIPE)

    test = subprocess.run("gpg --list-keys", shell=True, stdout=subprocess.PIPE)
    key_name = str([i for i in test.stdout.decode('utf-8').strip().split('\n') if i.startswith('uid')][0].split('] ')[1])
    log("key_name: " + key_name)

    commands = "gpg --output "+hass_options["pgp_public_key_path"]+".gpg --encrypt --trust-model always --recipient " + key_name + "  " + hass_options["pgp_public_key_path"]
    res = subprocess.run(commands, shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
    log("TESTING2: " + str(res))

def create_and_upload_backup():
    log('Creating backup...')
    res = requests.post('http://supervisor/backups/new/full', json = { "password": hass_options['backup_password'] } if 'backup_password' in hass_options.keys() else None, headers = { 'Authorization': 'Bearer ' + os.environ.get('SUPERVISOR_TOKEN') })
    if res.status_code == 200:
        log('Backup created successfully!')

        # Encrypt if needed
        if 'pgp_public_key' in hass_options.keys():
            log('Start encrypting backup...')
            log('Backup encrypting successfully!')

        log('Start uploading it to S3...')
        try:
            backup_path = f'/backup/{res.json()["data"]["slug"]}.tar'
            s3.upload_file(backup_path, hass_options['bucket_name'], f'{res.json()["data"]["slug"]}.tar')
            log('Backup uploaded successfully!')
            if hass_options['delete_local_backup_after_upload']:
                log('Deleting local backup...')
                os.remove(backup_path)
                log('Local backup deleted successfully!')
        except Exception as e:
            log('ERROR | Backup upload failed!')
            raise Exception(e)
    else:
        log('ERROR | Backup creation failed!')
        raise Exception(res.text)

encrypt_with_pgp()
while True:
    time.sleep(1)


#cron = croniter.croniter(hass_options['cron'], datetime.now())
#next_backup = cron.get_next(datetime)
#while True:
#    if datetime.now() >= next_backup:
#        create_and_upload_backup()
#        next_backup = cron.get_next(datetime)
#    time.sleep(10)
