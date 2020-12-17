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
from im.dingding import DingDing
from issues.BotJira import BotJira

from wechat.Bot import Bot

from db.BotDatabase import BotDatabase

from gerrit.BotGerrit import BotGerrit

review_message = "# [{}]({})\n" \
                 " \n" \
                 "> <font color=\"comment\">处理人：{}</font>\n\n" \
                 "> <font color=\"comment\">请帮忙review，有问题-1，没有问题+1</font>\n\n" \
                 "> {}\n" \
                 "\n" \
                 "\n\n备注：\n" \
                 " {}" \
                 "\n\n"

review_message_pi = "# [{}]({})\n" \
                    " \n" \
                    "> <font color=\"comment\">处理人：{}</font>\n\n" \
                    "> 请帮忙review，有问题-1，没有问题+1\n\n" \
                    "> {}\n" \
                    "\n" \
                    "\n\n备注：\n" \
                    " {}" \
                    "\n\n"


class BotReview(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.isRaspberryPi = Utils.isRaspberryPi()
        self.userConfig = Utils.readUserConfig()
        self.bot_key_test = self.userConfig["bot"]["bot_key_test"]
        self.botDatabase = BotDatabase()
        self.tableIssue = self.botDatabase.getTableIssue()
        self.access_token = self.userConfig["dingding"]["access_token"]
        self.secret = self.userConfig["dingding"]["secret"]

        self.gerritConfig = Utils.readGerritConfig()
        self.host_url_prv = self.gerritConfig['host_url_prv']
        self.project_url_game_dock = self.gerritConfig['project_url_game_dock']
        self.branch_name_game_dock_dev = self.gerritConfig['branch_name_game_dock_dev']
        self.host_url = self.gerritConfig['host_url']
        self.project_url_game_dock_engine = self.gerritConfig['project_url_game_dock_engine']

    def fetchIssues(self, sql):
        botJira = BotJira()
        botIssues = botJira.searchJql(sql)
        return botIssues

    def fetchGameDockPatchMessage(self, who):
        botGerrit = BotGerrit()
        botJira = BotJira()

        botPatchs = botGerrit.get_comment_patch_info_from_project(host_url=self.host_url_prv,
                                                                  project_url=self.project_url_game_dock,
                                                                  status='open',
                                                                  comment='need_review')
        for botPatch in botPatchs:
            flags = False
            result = self.tableIssue.find_one(issue=botPatch.number)
            print(datetime.datetime.now())
            if result is not None:
                if result["dock_team"] == 1:
                    print("dock team %s has been saved\n" % (botPatch.number))
                else:
                    flags = True
                    self.tableIssue.update(dict(issue=botPatch.number, dock_team=1, game_team=result["game_team"]),
                                           ["issue"])
                    print("dock team %s need save(update)\n" % (botPatch.number))
            else:
                flags = True
                self.tableIssue.insert(dict(issue=botPatch.number, dock_team=1, game_team=0))
                print("dock team %s need save\n" % (botPatch.number))

            if (flags):
                if self.isRaspberryPi:
                    message_format = review_message_pi
                else:
                    message_format = review_message

                issue = "Patch未填单号"
                link = "botPatch.url"

                if botPatch.issue != "null":
                    botIssue = botJira.searchIssue(botPatch.issue)
                    if botIssue is not None:
                        issue = botIssue.issue
                        link = botIssue.link

                message = message_format.format(issue, link, botPatch.owner_name, botPatch.url, botPatch.commitMessage)
                print(message)
                if self.isRaspberryPi:
                    ding = DingDing(self.access_token)
                    ding.set_secret(self.secret)
                    ding.send_markdown('Code review', message)
                else:
                    if who == "":
                        who = self.bot_key_test
                    bot = Bot(who)
                    bot.set_text(message, type='markdown').send()
                    bot.set_text('', type='text').set_mentioned_list(["@all"]).send()

    def fetchGameDockEnginePatchMessage(self, who):
        botGerrit = BotGerrit()
        botJira = BotJira()

        botPatchs = botGerrit.get_comment_patch_info_from_project(host_url=self.host_url,
                                                                  project_url=self.project_url_game_dock_engine,
                                                                  status='open',
                                                                  comment='need_review')
        for botPatch in botPatchs:
            flags = False
            result = self.tableIssue.find_one(issue=botPatch.number)
            print(datetime.datetime.now())
            if result is not None:
                if result["dock_team"] == 1:
                    print("dock team %s has been saved\n" % (botPatch.number))
                else:
                    flags = True
                    self.tableIssue.update(dict(issue=botPatch.number, dock_team=1, game_team=result["game_team"]),
                                           ["issue"])
                    print("dock team %s need save(update)\n" % (botPatch.number))
            else:
                flags = True
                self.tableIssue.insert(dict(issue=botPatch.number, dock_team=1, game_team=0))
                print("dock team %s need save\n" % (botPatch.number))

            if (flags):
                if self.isRaspberryPi:
                    message_format = review_message_pi
                else:
                    message_format = review_message

                issue = "Patch未填单号"
                link = "botPatch.url"

                if botPatch.issue != "null":
                    botIssue = botJira.searchIssue(botPatch.issue)
                    if botIssue is not None:
                        issue = botIssue.issue
                        link = botIssue.link

                message = message_format.format(issue, link, botPatch.owner_name, botPatch.url, botPatch.commitMessage)
                print(message)
                if self.isRaspberryPi:
                    ding = DingDing(self.access_token)
                    ding.set_secret(self.secret)
                    ding.send_markdown('Code review', message)
                else:
                    if who == "":
                        who = self.bot_key_test
                    bot = Bot(who)
                    bot.set_text(message, type='markdown').send()
                    bot.set_text('', type='text').set_mentioned_list(["@all"]).send()

    def notifyReview(self, who, sql):
        self.fetchGameDockPatchMessage(who)
        self.fetchGameDockEnginePatchMessage(who)
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
                    if self.isRaspberryPi:
                        message_format = review_message_pi
                    else:
                        message_format = review_message

                    message = message_format.format(botIssue.issue, botIssue.link,
                                                    botIssue.commentAuthor, botIssue.comment, "")
                    print(message)
                    if self.isRaspberryPi:
                        ding = DingDing(self.access_token)
                        ding.set_secret(self.secret)
                        ding.send_markdown('Code review', message)
                    else:
                        if who == "":
                            who = self.bot_key_test
                        bot = Bot(who)
                        bot.set_text(message, type='markdown').send()
                        bot.set_text('', type='text').set_mentioned_list(["@all"]).send()
