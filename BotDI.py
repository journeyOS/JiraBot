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

from base import Utils
from issues.BotJira import BotJira
from im.dingding import DingDing
from office.excel import WriteExcel
from wechat.Bot import Bot


TOTAL = "总数"
DI = [10, 3, 1, 0.1]
# ['致命', '严重', '一般', '提示', '总数', 'DI']

total_message = "# K-Pro 问题总数 = <font color=\"warning\">{}</font>\n" \
                "> 致命 = <font color=\"warning\">{}</font>\n" \
                "> 严重 = <font color=\"warning\">{}</font>\n" \
                "> 一般 = <font color=\"comment\">{}</font>\n" \
                "> 提示 = <font color=\"comment\">{}</font>\n" \
                "> 总DI = <font color=\"warning\">{}</font>\n\n"

sub_message = "## <font color=\"comment\">{}</font>问题总数 = <font color=\"warning\">{}</font>\n" \
              "> 致命 = <font color=\"warning\">{}</font>\n" \
              "> 严重 = <font color=\"warning\">{}</font>\n" \
              "> 一般 = <font color=\"comment\">{}</font>\n" \
              "> 提示 = <font color=\"comment\">{}</font>\n" \
              ">  DI = <font color=\"warning\">{}</font>\n\n"


class BotDI:

    def __init__(self):
        self.userConfig = Utils.readUserConfig()
        self.bot_key_test = self.userConfig["bot"]["bot_key_test"]
        self.access_token = self.userConfig["dingding"]["access_token"]
        self.secret = self.userConfig["dingding"]["secret"]

    def fetchIssues(self, sql):
        botJira = BotJira()
        botIssues = botJira.searchJql(sql)
        print(datetime.datetime.now())
        print('共 %d 个问题待解决' % len(botIssues))
        return botIssues

    def parseIssues(self, botIssues):
        datas = dict()
        datas[TOTAL] = [0, 0, 0, 0, 0, 0.0]

        for botIssue in botIssues:
            assignee = botIssue.assignee
            level = botIssue.level

            if assignee not in datas:
                datas[assignee] = [0, 0, 0, 0, 0, 0.0]

            if "致命" == level:
                # 致命+1
                datas[assignee][0] += 1
                # 总数+1
                datas[assignee][4] += 1
                # DI值+10
                datas[assignee][5] += DI[0]
                #######################
                # 致命+1
                datas[TOTAL][0] += 1
                # 总数+1
                datas[TOTAL][4] += 1
                # DI值+10
                datas[TOTAL][5] += DI[0]
            elif "严重" == level:
                datas[assignee][1] += 1
                # 总数+1
                datas[assignee][4] += 1
                # DI值+3
                datas[assignee][5] += DI[1]
                #######################
                datas[TOTAL][1] += 1
                # 总数+1
                datas[TOTAL][4] += 1
                # DI值+3
                datas[TOTAL][5] += DI[1]
            elif "一般" == level:
                datas[assignee][2] += 1
                # 总数+1
                datas[assignee][4] += 1
                # DI值+1
                datas[assignee][5] += DI[2]
                #######################
                datas[TOTAL][2] += 1
                # 总数+1
                datas[TOTAL][4] += 1
                # DI值+1
                datas[TOTAL][5] += DI[2]
            elif "提示" == level:
                datas[assignee][3] += 1
                # 总数+1
                datas[assignee][4] += 1
                # DI值+0.1
                datas[assignee][5] += DI[3]
                #######################
                datas[TOTAL][3] += 1
                # 总数+1
                datas[TOTAL][4] += 1
                # DI值+0.1
                datas[TOTAL][5] += DI[3]

        local_sub_message = ""
        for key, values in datas.items():
            print("key = %s , values = %s" % (key, values))
            if key != TOTAL:
                local_sub_message += sub_message.format(key, values[4], values[0], values[1], values[2], values[3],
                                                        values[5])

        last_message = total_message.format(datas[TOTAL][4], datas[TOTAL][0], datas[TOTAL][1],
                                            datas[TOTAL][2], datas[TOTAL][3], datas[TOTAL][5])
        # print(last_message + local_sub_message)
        return last_message + local_sub_message

    def writeIssues(self, botIssues):
        datas = dict()
        datas[TOTAL] = ["总数", 0, 0, 0, 0, 0, 0.0]

        for botIssue in botIssues:
            assignee = botIssue.assignee
            level = botIssue.level

            if assignee not in datas:
                datas[assignee] = ["总数", 0, 0, 0, 0, 0, 0.0]

            if "致命" == level:
                # 致命+1
                datas[assignee][1] += 1
                # 总数+1
                datas[assignee][5] += 1
                # DI值+10
                datas[assignee][6] += DI[0]
                #######################
                # 致命+1
                datas[TOTAL][1] += 1
                # 总数+1
                datas[TOTAL][5] += 1
                # DI值+10
                datas[TOTAL][6] += DI[0]
            elif "严重" == level:
                datas[assignee][2] += 1
                # 总数+1
                datas[assignee][5] += 1
                # DI值+3
                datas[assignee][6] += DI[1]
                #######################
                datas[TOTAL][2] += 1
                # 总数+1
                datas[TOTAL][5] += 1
                # DI值+3
                datas[TOTAL][6] += DI[1]
            elif "一般" == level:
                datas[assignee][3] += 1
                # 总数+1
                datas[assignee][5] += 1
                # DI值+1
                datas[assignee][6] += DI[2]
                #######################
                datas[TOTAL][3] += 1
                # 总数+1
                datas[TOTAL][5] += 1
                # DI值+1
                datas[TOTAL][6] += DI[2]
            elif "提示" == level:
                datas[assignee][4] += 1
                # 总数+1
                datas[assignee][5] += 1
                # DI值+0.1
                datas[assignee][6] += DI[3]
                #######################
                datas[TOTAL][4] += 1
                # 总数+1
                datas[TOTAL][5] += 1
                # DI值+0.1
                datas[TOTAL][6] += DI[3]

            datas[assignee][0] = assignee

        we = WriteExcel()
        l = []
        for key, values in datas.items():
            print("key = %s , values = %s" % (key, values))
            if key == TOTAL:
                total = values
            else:
                l.append(values)

        l.append(total)
        heads = ['致命', '严重', '一般', '提示', '个人总数', 'DI']
        we.writeData(sheet_name=time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time())), heads=heads, data=l)

    def notify(self, who, sql):
        botIssues = self.fetchIssues(sql)
        message = self.parseIssues(botIssues)
        print("\n")
        if who == "":
            who = self.bot_key_test
        bot = Bot(who)
        bot.set_text(message, type='markdown').send()

        ding = DingDing(self.access_token)
        ding.set_secret(self.secret)
        # ding.send_markdown('DI统计', message)

        # self.writeIssues(botIssues)
