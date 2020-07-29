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

from base import Singleton, Utils
from issues.BotJira import BotJira

from wechat.Bot import Bot

from db.BotDatabase import BotDatabase

review_message = "# [{}]({})\n" \
                 " \n" \
                 "> <font color=\"comment\">请帮忙review，有问题-1，没有问题+1</font>\n\n" \
                 "> {}\n\n"


class BotReview(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.userConfig = Utils.readUserConfig()
        self.bot_key_test = self.userConfig["bot"]["bot_key_test"]
        self.botDatabase = BotDatabase()
        self.tableIssue = self.botDatabase.getTableIssue()

    def fetchIssues(self, sql):
        botJira = BotJira()
        botIssues = botJira.searchJql(sql)
        return botIssues

    def notifyReview(self, who, sql):
        botIssues = self.fetchIssues(sql)
        for botIssue in botIssues:
            if "" != botIssue.comment:
                flags = False
                result = self.tableIssue.find_one(issue=botIssue.issue)
                print(datetime.datetime.now())
                if result is not None:
                    if result["dock_team"] == 1:
                        print("dock team %s has been saved\n" % (botIssue.issue))
                    else:
                        flags = True
                        self.tableIssue.update(dict(issue=botIssue.issue, dock_team=1, game_team=result["game_team"]),
                                               ["issue"])
                        print("dock team %s need save(update)\n" % (botIssue.issue))
                else:
                    flags = True
                    self.tableIssue.insert(dict(issue=botIssue.issue, dock_team=1, game_team=0))
                    print("dock team %s need save\n" % (botIssue.issue))

                if (flags):
                    message = review_message.format(botIssue.issue, botIssue.link, botIssue.comment)
                    print(message)
                    if who == "":
                        who = self.bot_key_test
                    bot = Bot(who)
                    bot.set_text(message, type='markdown').send()
