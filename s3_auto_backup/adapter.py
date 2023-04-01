import boto3
import requests
import time
import json
import os
from datetime import datetime

hass_options = json.load(open('/data/options.json'))
log = lambda value: os.system(f'echo \'{datetime.now().strftime("%m/%d/%Y, %H:%M:%S")} | {str(value)}\'') if hass_options["logging"] else lambda:None 


res = requests.get("http://supervisor/supervisor/ping", headers={ "Authorization": "Bearer " + os.environ.get('SUPERVISOR_TOKEN') })
log(f'GET: http://supervisor/supervisor/ping - status code: { res.status_code }')
log(f'GET: http://supervisor/supervisor/ping - text: { res.text }')

res = requests.post("http://supervisor/backups/new/full", headers={ "Authorization": "Bearer " + os.environ.get('SUPERVISOR_TOKEN') })

log(f'POST: http://supervisor/backups/new/full - status code: { res.status_code }')
log(f'POST: http://supervisor/backups/new/full - text: { res.text }')

# log(hass_options)

# s3 = boto3.client(
#     "s3",
#     aws_access_key_id=hass_options["public_key"],
#     aws_secret_access_key=hass_options["secret_key"]
# )
# s3.upload_file(
#     filename='my_file.zip', 
#     bucket=hass_options["bucket_name"], 
#     key='some_key'
# )