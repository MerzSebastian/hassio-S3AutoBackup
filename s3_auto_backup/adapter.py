import boto3
import requests
import time
import json
import subprocess
from datetime import datetime, timezone
import os
import croniter

hass_options = json.load(open('/data/options.json'))
log = lambda value: subprocess.run(f'echo "{datetime.now().strftime("%m/%d/%Y, %H:%M:%S")} | {str(value)}"', shell=True) if hass_options['logging'] else lambda: None
s3 = boto3.client('s3', aws_access_key_id = hass_options['access_key_id'], aws_secret_access_key = hass_options['secret_access_key'])

def create_and_upload_backup():
    log('Creating backup...')
    res = requests.post('http://supervisor/backups/new/full', json = { password: hass_options['backup_password'] } if 'backup_password' in hass_options.keys() else None, headers = { 'Authorization': 'Bearer ' + os.environ.get('SUPERVISOR_TOKEN') })
    if res.status_code == 200:
        log('Backup created successfully! Start uploading it to S3...')
        try:
            s3.upload_file(f'/backup/{res.json()["data"]["slug"]}.tar', hass_options['bucket_name'], f'{res.json()["data"]["slug"]}.tar')
            log('Backup uploaded successfully!')
        except Exception as e:
            log('ERROR | Backup upload failed! Exception: ' + str(e))
            raise Exception(e)
    else:
        log('ERROR | Backup creation failed!')
        raise Exception(res.text)

cron = croniter.croniter(hass_options['cron'], datetime.now())
next_backup = cron.get_next(datetime)
while True:
    if datetime.now() >= next_backup:
        create_and_upload_backup()
        next_backup = cron.get_next(datetime)
    time.sleep(10)
