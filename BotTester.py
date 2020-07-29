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

import datetime

from base import Singleton
from gerrit.BotGerrit import BotGerrit

from issues.BotJira import BotJira
from wechat.Bot import Bot

review_message = "{issue}: {title} \n" \
                 "---> 处理人: {owner}\n" \
                 "---> Jira地址: {issue_link}\n" \
                 "---> Gerrit地址: {patch_link}\n\n"


class BotTester(object):
    __metaclass__ = Singleton

    def notifyTester(self, who):
        botGerrit = BotGerrit()
        botJira = BotJira()
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)
        botPatchs = botGerrit.get_patch_info_from_file(yesterday)
        message = "%s GameDock模块合入问题数 = %d \n" \
                  "👇 👇 👇 👇 👇 👇 👇 👇 👇 👇 👇 👇 👇 👇 \n" % (yesterday, len(botPatchs))
        for botPatch in botPatchs:
            botIssue = botJira.searchIssue(botPatch.issue)
            message += review_message.format(issue=botPatch.issue,
                                             issue_link=botPatch.issue_link,
                                             owner=botPatch.owner_name,
                                             patch_link=botPatch.url,
                                             title=botIssue.title)

        print(datetime.datetime.now())
        print(message)

        bot = Bot(who)
        bot.set_text(message, type='text').send()
