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
import time

import requests
from base import Utils
from im.dingding import DingDing
from wechat.Bot import Bot

userConfig = Utils.readUserConfig()
bot_key_test = userConfig["bot"]["bot_key_test"]
access_token = userConfig["dingding"]["access_token"]
secret = userConfig["dingding"]["secret"]
user = userConfig["auth"]["user"]
pwd = userConfig["auth"]["pwd"]

message = "Welcome to the world of raspberry pi, device info = http://{ip}/pi-dashboard/\n"

host = "http://1.1.1.3"
endpoint = "/ac_portal/login.php"
url = ''.join([host, endpoint])
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
#     'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
#     'Accept-Encoding': 'gzip, deflate',
#     'Accept-Language': 'en-US,en;q=0.9,ja;q=0.8,zh-CN;q=0.7,zh;q=0.6',
#     'Accept': '*/*',
#     'Connection': 'keep-alive',
#     'Host': '1.1.1.3',
#     'Referer': 'http://1.1.1.3/ac_portal/default/pc.html?tabs=pwd',
#     'X-Requested-With': 'XMLHttpRequest'
# }
#
# body = {
#     "opr": "pwdLogin",
#     "userName": "********",
#     "pwd": "********",
#     "rememberPwd": 1
# }

if __name__ == '__main__':
    try:
        result = os.popen("iwgetid -r").readlines()[0].strip()
        print(result)
        if 'bskj-sh' == result:
            print("has connected bskj-sh wifi, need login user account")
            data = dict()
            data['opr'] = 'pwdLogin'
            data['rememberPwd'] = 1
            data['userName'] = user
            data['pwd'] = pwd
            r = requests.post(url, json.dumps(data))
            time.sleep(2)
    except:
        pass

    process = os.popen("hostname -I")
    outputs = process.readlines()
    for output in outputs:
        ip = output.strip()
        break

    print(ip)
    send_message = message.format(ip=ip)
    process.close()
    # bot = Bot(bot_key_test)
    # bot.set_text(send_message, type='text').send()

    ding = DingDing(access_token)
    ding.set_secret(secret)
    ding.send_text(send_message)
