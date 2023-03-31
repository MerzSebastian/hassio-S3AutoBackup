import boto3
import requests
import time
import json
import os


mqtt_response = requests.post("http://supervisor/backups/new/full", headers={
    "Authorization": "Bearer " + os.environ.get('SUPERVISOR_TOKEN')
}).json()["data"]

hass_options = json.load(open('/data/options.json'))


s3 = boto3.client('s3')
s3.upload_file('my_big_local_file.txt', 'some_bucket', 'some_key')