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

class Instance:
    def __init__(self, name, key, id, ip, date, state):
        self.name = name
        self.key = key
        self.id = id
        self.ip = ip
        self.date = date
        self.state = state

    def printInstance(self):
        """Print instance details"""
        printFormat = '|{0:20s}|{1:15s}|{2:19s}|{3:15s}|{4:19s}|{5:10s}|'
        print(printFormat.format(self.selfname, self.key, self.id, self.ip,
                self.date, self.state))

    def start(self):
        if self.state == 'stopped' :
            print("Starting the instance: {}....".format(self.name))
            command = ['aws', 'ec2', 'start-instances', '--instance-id', self.id]
            p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            data = p.stdout.read()

    def stop(self):
        if self.state == 'running' :
            print("Stopping the instance: {}....".format(self.name))
            command = ['aws', 'ec2', 'stop-instances', '--instance-id', self.id]
            p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            data = p.stdout.read()

