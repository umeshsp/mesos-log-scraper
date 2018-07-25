from urllib.request import urlopen
import json
import re
import pycurl
from io import BytesIO
import time
import os
import sys

url = os.getenv('MESOS_URL', 0)
# Set the environment variable MESOS_URL to the mesos container log link 
if url == 0:
    print ("  ------------------------------------------------------------------------------ ")
    print ("| Please set MESOS_URL in environment variable by running the following command |")
    print ("| export MESOS_URL=<mesos_url_link>                                             |")
    print ("  ------------------------------------------------------------------------------ ")
    sys.exit()
filtered_url = re.search('(.*?)stdout', url)
filtered_url_final = filtered_url.group(0)

raw_logs = urlopen(filtered_url_final + "&length=50000").read().decode(
    'utf-8')
filtered_logs = json.loads(raw_logs)

# Following code makes sure only the latest logs are displayed on the terminal 
if filtered_logs:
    previous_offset = filtered_logs['offset']

integer_previous_offset = int(previous_offset)

while True:
    raw_logs = urlopen(filtered_url_final + "&length=50000").read().decode(
        'utf-8')
    filtered_logs = json.loads(raw_logs)

    if filtered_logs:
        current_offset = filtered_logs['offset']

    integer_current_offset = int(current_offset)

    if integer_current_offset != integer_previous_offset:
        log_length = integer_current_offset - integer_previous_offset
        get_latest_logs_url = filtered_url_final + "&length=" + str(
            log_length) + "&offset=" + str(integer_previous_offset)
        buffer = BytesIO()  # type: bytes
        c = pycurl.Curl()
        c.setopt(c.URL, get_latest_logs_url)
        c.setopt(c.WRITEDATA, buffer)
        c.perform()
        c.close()
        body = buffer.getvalue().decode('UTF-8')
        response = json.loads(body)
        print(response['data'])
    integer_previous_offset = integer_current_offset