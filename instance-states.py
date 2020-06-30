#!/usr/bin/env python3.7

# BSD 3-Clause License
# 
# Copyright (c) 2020, SFU Computer Architecture Laboratory
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.



import sys
import json
import subprocess
from datetime import datetime, date, time
import dateutil.parser
import argparse


# Usage: python instance-states.py [key_name]
# Example 1: Show the instances of comaniac
#   python instance-states.py comaniac
# Example 2: Show all instances
#   python instance-states.py


def printInstances(Name):
    count = 0

    command = ['aws', 'ec2', 'describe-instances']
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    data = p.stdout.read()

    instanceData = (json.loads(data))['Reservations']

    tableFormat = '|{0:20s}|{1:15s}|{2:19s}|{3:15s}|{4:19s}|{5:10s}|'
    print('|' + '-' * 103 + '|')
    print(tableFormat.format('Name', 'KeyName', 'InstanceId', 'PublicIpAddress',
            'LaunchTime', 'State'))
    print('|' + '-' * 20 + '|' + '-' * 15 + '|' + 
    '-' * 19 + '|' + '-' * 15 + '|' + '-' * 19 + '|' + '-' * 10 + '|')

    for instance in instanceData:
        detail = instance['Instances'][0]
        state = detail['State']
        datetime = dateutil.parser.parse(detail['LaunchTime'])
        datetimeStr = datetime.strftime("%Y-%m-%d %H:%M:%S")
        key = detail['KeyName']
        inst_name = None
        if 'Tags' in detail:
            inst_name = detail['Tags'][0]['Value']

        if not Name or Name == inst_name:
            count += 1
            if 'PublicIpAddress' in detail:
                ip = detail['PublicIpAddress']
            else:
                ip = 'invalid'
            conv = lambda i : i or '<None>' 
            print(tableFormat.format(conv(inst_name), key, detail['InstanceId'], ip,
                    datetimeStr, state['Name']))

    print('|' + '-' * 103 + '|')
    print('Total {0} instances.'.format(count))



def main():
    # keyName = None
    parser = argparse.ArgumentParser(description="AWS Toolbox to manage instances")
    parser.add_argument("-l", "--print-list", help="Print the list of all aws instances", action='store_true')
    parser.add_argument("--name", help="Input Instance name to search", default=None)
    args = parser.parse_args()
    if(args.print_list):
        printInstances(args.name)


if __name__ == "__main__":
    main()
