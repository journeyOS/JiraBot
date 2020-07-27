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

# https://jira.readthedocs.io/en/master/examples.html
from jira import JIRA

from base import Utils, Singleton
from issues.BotIssue import BotIssue


class BotJira(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.userConfig = Utils.readUserConfig()
        self.jiraConfig = Utils.readJiraConfig()
        self.jiraService = self.jiraConfig['jira_service']
        self.jiraUser = self.userConfig['auth']['user']
        self.jiraPwd = self.userConfig['auth']['pwd']
        self.jiraFields = self.jiraConfig['jira_fields']
        self.jira = JIRA(server=self.jiraService, basic_auth=(self.jiraUser, self.jiraPwd))

    def searchJql(self, jql):
        botIssues = list()
        issues = self.jira.search_issues(jql, fields=self.jiraFields)
        # issues = self.jira.search_issues(jql, fields=None)
        for issue in issues:
            botIssue = BotIssue(self.jiraService, issue)
            botIssues.append(botIssue)
        return botIssues

    def searchIssue(self, search_issue):
        result = self.jira.issue(search_issue, fields=self.jiraFields)
        return BotIssue(self.jiraService, result)
