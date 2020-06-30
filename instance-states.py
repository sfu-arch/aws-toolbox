#!/usr/bin/env python3.7
import sys
import json
import subprocess
from datetime import datetime, date, time
import dateutil.parser

# Usage: python instance-states.py [key_name]
# Example 1: Show the instances of comaniac
#   python instance-states.py comaniac
# Example 2: Show all instances
#   python instance-states.py

count = 0
keyName = None
if len(sys.argv) == 2:
    keyName = sys.argv[1]

command = ['aws', 'ec2', 'describe-instances']
p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
data = p.stdout.read()

instanceData = (json.loads(data))['Reservations']


for instance in instanceData:
    detail = instance['Instances'][0]
    if 'Tags' in detail:
        print(detail['Tags'][0]['Value'])
    else:
        'None'

tableFormat = '{0:20s}|{1:15s}|{2:19s}|{3:15s}|{4:19s}|{5:10s}'
print(tableFormat.format('Name', 'KeyName', 'InstanceId', 'PublicIpAddress',
        'LaunchTime', 'State'))

for instance in instanceData:
    detail = instance['Instances'][0]
    state = detail['State']
    datetime = dateutil.parser.parse(detail['LaunchTime'])
    datetimeStr = datetime.strftime("%Y-%m-%d %H:%M:%S")
    key = detail['KeyName']
    name = '<None>'
    if 'Tags' in detail:
        name = detail['Tags'][0]['Value']

    if not keyName or keyName == key:
        count += 1
        if 'PublicIpAddress' in detail:
            ip = detail['PublicIpAddress']
        else:
            ip = 'invalid'
        print(tableFormat.format(name, key, detail['InstanceId'], ip,
                datetimeStr, state['Name']))

print('Total {0} instances.'.format(count))
