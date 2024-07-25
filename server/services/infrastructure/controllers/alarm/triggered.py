from server.common.controller import BaseController
from server.connectors.jira_connector.incident import JiraIncident
from server.connectors.newrelic.incident import NewRelicIncident
from server.util import get_logger


class TriggeredAlarms(BaseController):
    def __init__(self):
        super().__init__()
        self.name = 'TriggeredAlarms'
        self.methods = ['list', 'view']
        self.logger = get_logger(__class__.__name__)

        self.customer_info = {}

        self.jira_incident = JiraIncident()
        self.newrelic_incident = NewRelicIncident()

    def load_customer_info(self, nr_account_name: str, db):
        if nr_account_name in self.customer_info:
            return self.customer_info[nr_account_name]

        condition = {'Organization_NAME': nr_account_name}

        success, nr_account = db.get_rows('newrelic_organizations', where_items=[condition])

        if not success:
            self.logger.error(f"Failed to get customer info for {nr_account_name}")
            return None

        self.customer_info[nr_account_name] = {
            'nr_id': nr_account[0]['Organization_ID'],
            'sub_client_id': nr_account[0]['Sub_Client_ID'],
            'nr_name': nr_account[0]['Organization_NAME'],
        }

        return self.customer_info[nr_account_name]

    def list(self, payload: dict):
        results, status_code = self.jira_incident.list(payload)

        return results, status_code

    def view(self, payload: dict):
        db = payload.get('db')
        alarm = payload.get('data')

        nr_account_name = alarm.get('NewRelic Account')

        nr_account = self.load_customer_info(nr_account_name, db)

        nr_incident, status_code = self.newrelic_incident.view({'data': {'title': alarm.get('Title'),
                                                                         'account_id': nr_account['nr_id']}})

        print(nr_incident)

        return alarm, 200

