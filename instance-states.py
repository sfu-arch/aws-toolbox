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
import instance

def getInstances(Name):
    count = 0

    command = ['aws', 'ec2', 'describe-instances']
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    data = p.stdout.read()

    instanceData = (json.loads(data))['Reservations']

    ret_instances = []
    for inst in instanceData:
        detail = inst['Instances'][0]
        state = detail['State']
        datetime = dateutil.parser.parse(detail['LaunchTime'])
        datetimeStr = datetime.strftime("%Y-%m-%d %H:%M:%S")
        key = detail['KeyName']
        inst_name = None
        if 'Tags' in detail:
            inst_name = detail['Tags'][0]['Value']

        if not Name or Name == inst_name:
            count += 1
            conv = lambda i : i or '<None>' 
            if 'PublicIpAddress' in detail:
                ip = detail['PublicIpAddress']
            else:
                ip = 'invalid'
            new_instance = instance.Instance(conv(inst_name), key, detail['InstanceId'], ip,
                datetimeStr, state['Name'])
            ret_instances.append(new_instance)

    return ret_instances

def printInstances(instanceData):
    count = 0
    tableFormat = '|{0:20s}|{1:15s}|{2:19s}|{3:15s}|{4:19s}|{5:10s}|'
    print('|' + '-' * 103 + '|')
    print(tableFormat.format('Name', 'KeyName', 'InstanceId', 'PublicIpAddress',
            'LaunchTime', 'State'))
    print('|' + '-' * 103 + '|')

    for inst in instanceData:
        count += 1
        print(tableFormat.format(inst.name, inst.key, inst.id, inst.ip,
                inst.date, inst.state))

    print('|' + '-' * 103 + '|')
    print('Total {0} instances.'.format(count))


def printStatus(instanceData):

    tableFormat = '|{0:20s}|{1:15s}|'
    print('|' + '-' * 36 + '|')
    print(tableFormat.format('Name', 'Status'))
    print('|' + '-' * 36 + '|')

    for inst in instanceData:
        print(tableFormat.format(inst.name, inst.state))

    print('|' + '-' * 36 + '|')



def main():
    parser = argparse.ArgumentParser(description="AWS Toolbox to manage instances")
    exe_group = parser.add_mutually_exclusive_group()

    parser.add_argument("-l", "--print-list", help="Print the list of all aws instances", action='store_true')
    parser.add_argument("-s", "--status", help="Print the the status of the instances", action='store_true', default=False)
    parser.add_argument("--name", help="Input Instance name to search", default=None)
    parser.add_argument("--afi", help="Check AFI images", action='store_true', default=False)


    exe_group.add_argument("--start", help="Run the searched instance", action='store_true')
    exe_group.add_argument("--stop", help="Stop the searched instance", action='store_true')



    args = parser.parse_args()
    if(args.status):
        instances = getInstances(args.name)
        printStatus(instances)
    if(args.print_list):
        instances = getInstances(args.name)
        printInstances(instances)
    if(args.start):
        instances = getInstances(args.name)
        for instance in instances:
            instance.start()
    if(args.stop):
        instances = getInstances(args.name)
        for instance in instances:
            instance.stop()
    if(args.afi):
        # instances = getInstances(args.name)
        # for instance in instances:
        #     instance.stop()

if __name__ == "__main__":
    main()
