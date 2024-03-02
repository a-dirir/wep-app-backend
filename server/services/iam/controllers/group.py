

class Group:
    def __init__(self):
        self.table_name = 'iam_groups'

    def create(self, payload: dict):
        data = payload['data']
        db = payload['db']

        # add validation

        row = {
            'name': data['name'],
            'description': data['description'],
            'policy': data['policy']
        }

        # insert row into table
        success, results = db.insert_row(table_name=self.table_name, row=row)

        if not success:
            return {'error': results}, 400

        return row, 200

    def get(self, payload: dict):
        data = payload['data']
        db = payload['db']

        # add validation

        # get row from table
        conditions = {'name': data['name']}
        success, results = db.get_row(table_name=self.table_name, where_items=conditions)

        if not success:
            return {'error': results}, 400

        return results, 200

    def list(self, payload: dict):
        db = payload['db']

        # get all rows from table
        success, results = db.get_rows(table_name=self.table_name)

        if not success:
            return {'error': results}, 400

        return results, 200

    def update(self, payload: dict):
        data = payload['data']
        db = payload['db']

        # add validation

        # update row in table
        conditions = {'name': data['name']}
        data.pop('name')
        success, results = db.update_row(table_name=self.table_name, row=data, where_items=conditions)

        if not success:
            return {'error': results}, 400

        return results, 200

    def delete(self, payload: dict):
        data = payload['data']
        db = payload['db']

        # add validation

        # delete row from table
        conditions = {'name': data['name']}
        success, results = db.delete_row(table_name=self.table_name, where_items=conditions)

        if not success:
            return {'error': results}, 400

        return results, 200






