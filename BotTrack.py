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
from issues.BotJira import BotJira

from wechat.Bot import Bot

review_message = "# [{}]({})\n" \
                 " \n" \
                 "> <font color=\"comment\">有问题需要处理</font>\n\n"


class BotTrack(object):
    __metaclass__ = Singleton

    def fetchIssues(self, sql):
        botJira = BotJira()
        botIssues = botJira.searchJql(sql)
        print(datetime.datetime.now())
        print('共 %d 个问题需要track\n' % len(botIssues))
        return botIssues

    def notifyTrack(self, sql, who):
        botIssues = self.fetchIssues(sql)
        for botIssue in botIssues:
            message = review_message.format(botIssue.issue, botIssue.link)
            print(message)
            bot = Bot(who)
            bot.set_text(message, type='markdown').send()
