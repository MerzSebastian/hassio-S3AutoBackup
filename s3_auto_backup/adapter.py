import boto3
import requests
import time
import json
import os


log = lambda x: os.system('echo ' + x)

res = requests.post("http://supervisor/backups/new/full", headers={
    "Authorization": "Bearer " + os.environ.get('SUPERVISOR_TOKEN')
})
log(res.status_code)
log(res.text)

hass_options = json.load(open('/data/options.json'))
log(hass_options)


s3 = boto3.client('s3')
s3.upload_file('my_big_local_file.txt', 'some_bucket', 'some_key')