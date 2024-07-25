from datetime import datetime
import re
import ast

from server.common.controller import BaseController
from server.connectors.newrelic.agent import NewRelicAgent


class NewRelicIncident(BaseController):
    def __init__(self):
        super().__init__()
        self.agent = NewRelicAgent()
        self.methods = ['list', 'view']
        self.accounts = []

    def list(self, payload: dict):
        account_id = payload['data']['account_id']

        incidents = self.agent.get_alert_incidents(account_id)

        if incidents is None:
            return 'Failed to get incidents', 400

        processed_incidents = self.process_row_incidents(incidents)

        return {'data': processed_incidents}, 200

    @staticmethod
    def process_row_incidents(incidents: list):
        processed_incidents = []

        for incident in incidents:
            processed_incident = {
                'Title': ast.literal_eval(incident['title'])[-1],
                'Resource': incident['entityNames'],
                'Entity Guids': incident['entityGuids'],
                'Incident Id': incident['incidentId'],
            }

            description = re.search(r"Condition: '([^']*)'", incident['description'][-1])

            if description is not None:
                processed_incident['Condition'] = description.group(1)
            else:
                processed_incident['Condition'] = 'No condition found'

            # convert createdAt and updatedAt to datetime objects from milliseconds
            created_at = datetime.fromtimestamp(incident['createdAt'] / 1000.0)
            processed_incident['Date Created'] = created_at.strftime('%Y-%m-%d')
            processed_incident['Time Created'] = created_at.strftime('%H:%M')

            processed_incidents.append(processed_incident)

        return processed_incidents

    def view(self, payload: dict):
        title = payload['data']['title']

        incidents, status_code = self.list(payload)

        if status_code == 400:
            return 'Failed to get incidents', 400

        incidents = incidents['data']

        for incident in incidents:
            if incident['Title'] == title:
                return incident, 200

        return 'Incident not found', 404