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


import os

from base import Utils
from wechat.Bot import Bot

userConfig = Utils.readUserConfig()
bot_key_test = userConfig["bot"]["bot_key_test"]

message = "Welcome to the world of raspberry pi, device ip = {ip}\n"

if __name__ == '__main__':
    process = os.popen("hostname -I")
    outputs = process.readlines()
    for output in outputs:
        ip = output.strip()
        break

    print(ip)
    process.close()
    bot = Bot(bot_key_test)
    bot.set_text(message.format(ip=ip), type='text').send()
