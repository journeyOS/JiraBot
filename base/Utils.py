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

import json
import os


def realPath(path):
    return os.path.join(os.path.dirname(__file__), path)


def readUserConfig():
    with open(realPath("../config/user.json"), 'r') as f:
        config = f.read()
    return json.loads(config)


def readJiraConfig():
    with open(realPath("../config/jira.json"), 'r') as f:
        config = f.read()
    return json.loads(config)


def readSendIssues():
    with open(realPath("../cache/send_issuse.txt"), 'r') as f:
        issues = f.readlines()
    return issues


def writeSendIssues(issue):
    with open(realPath("../cache/send_issuse.txt"), 'a') as f:
        f.write(issue + '\n')


def readMergeCode():
    with open(realPath("../cache/merge_code.txt"), 'r') as f:
        issues = f.readlines()
    return issues


def writeMergeCode(issue):
    with open(realPath("../cache/merge_code.txt"), 'a') as f:
        f.write(issue + '\n')
