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

import threading
import time

import schedule as schedule

from BotDI import BotDI
from BotMergeCode import BotMergeCode
from BotReview import BotReview
from BotTester import BotTester
from BotTrack import BotTrack
from base import Utils

botDI = BotDI()
botReview = BotReview()
botMergeCode = BotMergeCode()
botTrack = BotTrack()
botTester = BotTester()

userConfig = Utils.readUserConfig()
jiraConfig = Utils.readJiraConfig()
gerritConfig = Utils.readGerritConfig()

bot_key_test = userConfig["bot"]["bot_key_test"]
bot_key_game_dock = userConfig["bot"]["bot_key_game_dock"]
bot_key_tester = userConfig["bot"]["bot_key_tester"]

jira_game_dock_jql = jiraConfig['jira_game_dock_jql']
jira_track = jiraConfig['jira_track']
jira_jql_review = jiraConfig['jira_jql_review']
jira_jql_game_team_push_mp = jiraConfig['jira_jql_game_team_push_mp']

host_url_prv = gerritConfig['host_url_prv']
project_url_game_dock = gerritConfig['project_url_game_dock']
branch_name_game_dock_dev = gerritConfig['branch_name_game_dock_dev']
branch_name_game_dock_mp = gerritConfig['branch_name_game_dock_mp']
host_url = gerritConfig['host_url']
project_url_game_dock_engine = gerritConfig['project_url_game_dock_engine']
branch_name_game_dock_engine_dev = gerritConfig['branch_name_game_dock_engine_dev']


def jobDI():
    botDI.notify(bot_key_game_dock, jira_game_dock_jql)


def jobDITest():
    botDI.notify(bot_key_test, jira_game_dock_jql)


def jobReview():
    botReview.notifyReview(bot_key_game_dock, jira_jql_review)


def jobMergeCode():
    botMergeCode.notifyMergeCode(bot_key_test, jira_jql_game_team_push_mp, force=False)


def jobTrack():
    botTrack.notifyTrack(jira_track, bot_key_test)


def jobTester():
    botTester.notifyTester(bot_key_test, host_url_prv, project_url_game_dock, branch_name_game_dock_dev)
    botTester.notifyTester(bot_key_test, host_url_prv, project_url_game_dock, branch_name_game_dock_mp)

    botTester.notifyTester(bot_key_tester, host_url_prv, project_url_game_dock, branch_name_game_dock_dev)


def runThreaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()


for i in ["10:00", "17:30"]:
    schedule.every().monday.at(i).do(runThreaded, jobDI)
    schedule.every().tuesday.at(i).do(runThreaded, jobDI)
    schedule.every().wednesday.at(i).do(runThreaded, jobDI)
    schedule.every().thursday.at(i).do(runThreaded, jobDI)
    schedule.every().friday.at(i).do(runThreaded, jobDI)

botTesterTime = "10:00"
schedule.every().monday.at(botTesterTime).do(runThreaded, jobTester)
schedule.every().tuesday.at(botTesterTime).do(runThreaded, jobTester)
schedule.every().wednesday.at(botTesterTime).do(runThreaded, jobTester)
schedule.every().thursday.at(botTesterTime).do(runThreaded, jobTester)
schedule.every().friday.at(botTesterTime).do(runThreaded, jobTester)

schedule.every(5).minutes.do(runThreaded, jobReview)

schedule.every(5).minutes.do(runThreaded, jobMergeCode)

schedule.every(3).hours.do(runThreaded, jobTrack)

if __name__ == '__main__':
    jobDITest()

    # jobTester()
    botTester.notifyTester(bot_key_test, host_url_prv, project_url_game_dock, branch_name_game_dock_dev)
    botTester.notifyTester(bot_key_test, host_url_prv, project_url_game_dock, branch_name_game_dock_mp)

    botMergeCode.notifyMergeCode(bot_key_test, jira_jql_game_team_push_mp, force=True)
    jobReview()
    jobMergeCode()
    jobTrack()
    while True:
        schedule.run_pending()
        time.sleep(5)
