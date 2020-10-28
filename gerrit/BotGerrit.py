#  !/usr/bin/env python
#  -*- encoding: utf-8 -*-
#
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.


import json
import os

from base import Singleton
from gerrit.BotPatch import BotPatch


class BotGerrit(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.base_host = "ssh -p 29418 {host} gerrit query project:{project} --format=JSON branch:{branch} status:{status} after:{yesterday} before:{today} "
        self.comment_host = "ssh -p 29418 {host} gerrit query project:{project} --format=JSON status:{status} label:Code-Review+1,user=jenkins@blackshark.com label:Verified+1,user=jenkins@blackshark.com comment:{comment}"
        self.file = "{pwd}/cache/{time}.txt"

    def get_patch_info_from_project(self, host_url, project_url, branch_name, status, yesterday, today):
        cmd = self.base_host.format(host=host_url, project=project_url, branch=branch_name,
                                    status=status, yesterday=yesterday, today=today)
        print(cmd)
        process = os.popen(cmd)
        outputs = process.readlines()

        del outputs[-1]  # 删除最后一个元素
        patchs = list()
        for output in outputs:
            result = json.loads(output)
            patchs.append(BotPatch(result))
        process.close()
        return patchs

    def get_comment_patch_info_from_project(self, host_url, project_url, status, comment):
        cmd = self.comment_host.format(host=host_url, project=project_url, status=status, comment=comment)
        print(cmd)
        process = os.popen(cmd)
        outputs = process.readlines()

        del outputs[-1]  # 删除最后一个元素
        patchs = list()
        for output in outputs:
            result = json.loads(output)
            patchs.append(BotPatch(result))
        process.close()
        return patchs

    def get_patch_info_from_file(self, today):
        print(os.getcwd())
        patchs = list()
        try:
            fileName = self.file.format(pwd=os.getcwd(), time=today)
            f2 = open(fileName, 'r')
            for output in f2.readlines():
                # print(output)
                result = json.loads(output)
                patchs.append(BotPatch(result))
        except:
            pass
        os.system("rm -rf %s" % fileName)
        return patchs
