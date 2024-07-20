from os import getenv
from jira import JIRA
import datetime
from server.common.controller import BaseController
from server.util import get_logger


class JiraIncidents(BaseController):
    def __init__(self):
        super().__init__()
        self.name = 'JiraIncidents'
        self.methods = ['list']
        self.logger = get_logger(__class__.__name__)

    def list(self):
        jira_options = {'server': getenv("JIRA_URL")}
        jira_connector = JIRA(options=jira_options, basic_auth=(getenv("JIRA_USER"), getenv("JIRA_API_KEY")))

        jira_jql = """
            type = Incident
            AND status IN ("To Do", "In Progress")
            AND created >= -2h
            AND reporter = 712020:6fd94ad0-4cc0-4126-8918-07e320c26f65
            ORDER BY created DESC
        """

        issues = []
        try:
            for issue in jira_connector.search_issues(jira_jql, maxResults=False):
                timestamp = datetime.datetime.strptime(issue.fields.created, '%Y-%m-%dT%H:%M:%S.%f%z')
                time = timestamp.strftime('%H:%M:%S')
                date = timestamp.date().isoformat()

                # summary comes in the formate condition on resource
                summary = issue.fields.summary
                # remove [Re-Triggered] or [Triggered] or [No-Data] and space in the beginning from summary if present
                summary = summary.split('] ')[-1]
                summary = summary.strip()
                condition = summary.split(' on ')[0]
                resource = summary.split(' on ')[1]

                issue_dict = {
                    'Issue Key': issue.key,
                    'Summary': summary,
                    'Condition': condition,
                    'Resource': resource,
                    'Title': issue.fields.description.split('\n')[0],
                    'NewRelic Account': issue.fields.customfield_10354,
                    'Date': date,
                    'Time': time
                }

                issues.append(issue_dict)
        except Exception as e:
            self.logger.error(f"Failed to get Jira incidents {e}")
            return [], 400

        return issues, 200
