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

from wechat.Bot import Bot
from base import Utils

# message = "# [KASE-6220](http://jira.blackshark.com/browse/KASE-6220)\n" \
#           " \n" \
#           "> <font color=\"comment\">处理人：黄安棋</font>\n\n" \
#           "> <font color=\"comment\">请帮忙review，有问题-1，没有问题+1</font>\n\n" \
#           "> http://gerrit-prv.blackshark.com:8080/120691\n" \
#           "\n" \
#           "\n\n备注：\n" \
#           " kaiser/penrose项目使用小米的接口设置WLAN低延迟模式" \
#           "\n\n"
message = "Davis 的机器人跑起来了～"

if __name__ == '__main__':
    userConfig = Utils.readUserConfig()
    # who = userConfig["bot"]["bot_key_test"]
    who = userConfig["bot"]["bot_key_game_dock"]
    bot = Bot("66ec8cec-7c1e-41d0-9712-f00a62e831c8")
    bot.set_text("Davis 的机器人跑起来了～", type='markdown').send()
    bot.set_text('', type='text').set_mentioned_list(["@all"]).send()
