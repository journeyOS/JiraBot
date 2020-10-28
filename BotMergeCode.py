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
import time

from base import Singleton, Utils
from im.dingding import DingDing
from issues.BotJira import BotJira

from wechat.Bot import Bot

from db.BotDatabase import BotDatabase

comment_message = "#{count} : {who}\n" \
                  "{comment}\n\n"

author_message = "{who} : 提交{count}笔\n"

total_message_count = "\n总计提交 : {count}笔\n"

time_message = "截止{time}, 需要合入提交一共 : {count}笔\n\n"


class BotMergeCode(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.isRaspberryPi = Utils.isRaspberryPi()
        self.userConfig = Utils.readUserConfig()
        self.bot_key_test = self.userConfig["bot"]["bot_key_test"]
        self.botDatabase = BotDatabase()
        self.tableIssue = self.botDatabase.getTableIssue()
        self.access_token = self.userConfig["dingding"]["access_token"]
        self.secret = self.userConfig["dingding"]["secret"]

    def fetchIssues(self, sql):
        botJira = BotJira()
        botIssues = botJira.searchJql(sql)
        return botIssues

    def notifyMergeCode(self, who, sql, force):
        botIssues = self.fetchIssues(sql)
        datas = dict()
        issue_count = 0
        total_comment_message = ""
        total_author_message = ""

        if force:
            flags = False
        else:
            flags = True

        for botIssue in botIssues:
            if "" != botIssue.comment:
                if (flags):
                    result = self.tableIssue.find_one(issue=botIssue.issue)
                    print(datetime.datetime.now())
                    if result is not None:
                        if result["game_team"] == 1:
                            print("game team %s has been saved\n" % (botIssue.issue))
                        else:
                            flags = False
                            self.tableIssue.update(
                                dict(issue=botIssue.issue, dock_team=result["dock_team"], game_team=1), ["issue"])
                            print("game team %s need save(update)\n" % (botIssue.issue))
                    else:
                        flags = False
                        self.tableIssue.insert(dict(issue=botIssue.issue, dock_team=0, game_team=1))
                        print("game team %s need save\n" % (botIssue.issue))

                if botIssue.commentAuthor not in datas:
                    datas[botIssue.commentAuthor] = [0]

                datas[botIssue.commentAuthor][0] += 1
                issue_count += 1

                total_comment_message = total_comment_message + comment_message.format(count=str(issue_count),
                                                                                       who=botIssue.commentAuthor,
                                                                                       comment=botIssue.comment)
        for key, values in datas.items():
            # print("key = %s , values = %s" % (key, values))
            count = str(values)
            total_author_message = total_author_message + author_message.format(who=key, count=count)

        total_message = time_message.format(time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), count=str(
            issue_count)) + total_comment_message + total_message_count.format(
            count=str(issue_count)) + total_author_message

        if flags:
            print(datetime.datetime.now())
            print("game team has been notify\n")
        else:
            print(total_message)
            if issue_count > 0:
                if self.isRaspberryPi:
                    ding = DingDing(self.access_token)
                    ding.set_secret(self.secret)
                    ding.send_text(total_message)
                else:
                    if who == "":
                        who = self.bot_key_test
                    bot = Bot(who)
                    bot.set_text(total_message, type='text').send()
