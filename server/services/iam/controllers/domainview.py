from server.common.controller import BaseController


class DomainView(BaseController):
    def __init__(self):
        super().__init__()
        self.name = 'DomainView'
        self.methods = ['list']

        self.domains = {
            'SubClient': {
                'table_name': 'sub_clients',
                'columns': ['Sub_Client_ID', 'Name'],
                'values': None
            },
            'NewRelic': {
                'table_name': 'newrelic_organizations',
                'columns': ['Organization_ID', 'Organization_NAME'],
                'values': None
            },
        }

    def list(self, payload: dict):
        db = payload['db']

        # get the domain from the payload
        domain_name = payload['data']['domain_name']

        # get the domain details
        domain_details = self.domains.get(domain_name)

        # get the rows from the database
        success, results = db.get_rows(table_name=domain_details['table_name'], columns=domain_details['columns'])

        if not success:
            return {'error': 'Failed to get the domain details'}, 400

        # map the results to the domain values and return
        data = []
        for result in results:
            data.append({'ID': result[domain_details['columns'][0]], 'Name': result[domain_details['columns'][1]]})

        self.domains[domain_name]['values'] = data

        return {'data': data}, 200
