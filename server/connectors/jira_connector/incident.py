from os import getenv
from jira import JIRA
from datetime import datetime, timedelta
import math
from server.util import get_logger


class JiraIncident:
    def __init__(self):
        self.name = 'JiraIncident'
        self.logger = get_logger(__class__.__name__)

    @staticmethod
    def hours_since_shift_start():
        current_time = datetime.now()

        shifts = [
            datetime(current_time.year, current_time.month, current_time.day, 7, 0),  # 07:00 AM
            datetime(current_time.year, current_time.month, current_time.day, 15, 0),  # 03:00 PM
            datetime(current_time.year, current_time.month, current_time.day, 23, 0)  # 11:00 PM
        ]

        if current_time < shifts[0]:
            current_shift_start = shifts[2] - timedelta(days=1)  # Last shift of the previous day
        elif current_time < shifts[1]:
            current_shift_start = shifts[0]
        elif current_time < shifts[2]:
            current_shift_start = shifts[1]
        else:
            current_shift_start = shifts[2]

        hours_diff = (current_time - current_shift_start).total_seconds() / 3600.0

        return math.ceil(hours_diff)

    def list(self, payload: dict):
        jira_options = {'server': getenv("JIRA_URL")}
        jira_connector = JIRA(options=jira_options, basic_auth=(getenv("JIRA_USER"), getenv("JIRA_API_KEY")))

        # hours_since_shift_start = self.hours_since_shift_start()
        hours_since_shift_start = 1

        jira_jql = f"""
            type = Incident
            AND status IN ("To Do", "In Progress")
            AND created >= -{hours_since_shift_start}h
            AND reporter = 712020:6fd94ad0-4cc0-4126-8918-07e320c26f65
            ORDER BY created DESC
        """

        issues = []
        try:
            for issue in jira_connector.search_issues(jira_jql, maxResults=False):
                timestamp = datetime.strptime(issue.fields.created, '%Y-%m-%dT%H:%M:%S.%f%z')
                time = timestamp.strftime('%H:%M:%S')
                date = timestamp.date().isoformat()

                # summary comes in the format condition on resource
                summary = issue.fields.summary
                # remove [Re-Triggered] or [Triggered] or [No-Data] and space in the beginning from summary if present
                if "[No-Data]" in summary:
                    continue

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
            return {'error': f"Failed to get Jira incidents {e}"}, 400

        return {'data': issues}, 200
