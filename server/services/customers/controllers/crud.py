from server.services.customers.models.services_mappings import services_mappings


class CRUD:
    def __init__(self):
        self.services_mappings = services_mappings

    def create(self, payload: dict):
        data = payload['data']
        db = payload['db']

        # get service name
        if data.get('service') is None:
            return {'error': 'Service name is missing'}, 400

        if self.services_mappings.get(data['service']) is None:
            return {'error': 'Service name is invalid'}, 400

        table_name = self.services_mappings[data['service']]

        # prepare and validate data
        row = data

        # insert row into table
        status, results = db.insert_row(table_name=table_name, row=row)

        if not status:
            return {'error': results}, 400

        return results, 200

    def read(self, payload: dict):
        data = payload['data']
        db = payload['db']

        # get service name
        if data.get('service') is None:
            return {'error': 'Service name is missing'}, 400

        if self.services_mappings.get(data['service']) is None:
            return {'error': 'Service name is invalid'}, 400

        table_name = self.services_mappings[data['service']]

        # prepare where clause
        conditions = data.get('conditions', None)
        distinct = data.get('distinct', "")
        columns = data.get('columns', None)

        # get all rows from table
        status, results = db.get_rows(table_name=table_name, columns=columns, where_items=conditions, distinct=distinct)
        if not status:
            return {'error': results}, 400

        return results, 200

    def list(self, payload: dict):
        data = payload['data']
        db = payload['db']

        # get service name
        service = data['service']
        table_name = self.services_mappings[service]

        # get all rows from table
        status, results = db.get_rows(table_name=table_name)
        if not status:
            return {'error': results}, 400

        return results, 200

    def update(self, id, data):
        return self.model.update(id, data)

    def delete(self, id):
        return self.model.delete(id)