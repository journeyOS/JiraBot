#  !/usr/bin/env python
#  -*- encoding: utf-8 -*-
#
#  Copyright (c) 2020 anqi.huang@outlook.com
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

import re


class BotPatch:

    def __init__(self, result):
        # 单号
        self.issue = re.findall(re.compile(r'[[](.*?)[]]', re.S), result['subject'])[0]
        # 单号地址
        self.issue_link = "http://jira.blackshark.com/browse/" + self.issue
        # 提交人
        self.owner_name = result["owner"]["name"].replace('BP', '')
        # patch地址
        self.url = result["url"]
        # branch
        self.branch = result["branch"]
        # status
        self.status = result["status"]

        def __str__(self):
            print(['%s:%s' % item for item in self.__dict__.items()])
