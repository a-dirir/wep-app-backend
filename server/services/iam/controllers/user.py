

class User:
    def __init__(self):
        self.table_name = 'iam_users'

    def create(self, payload: dict):
        data = payload['data']
        db = payload['db']

        # add validation

        # insert row into table
        success, results = db.insert_row(table_name=self.table_name, row=data)

        if not success:
            return {'error': results}, 400

        return results, 200

    def get(self, payload: dict):
        data = payload['data']
        db = payload['db']

        # add validation

        # get row from table
        conditions = {'email': data['email']}
        success, results = db.get_row(table_name=self.table_name, where_items=conditions)

        if not success:
            return {'error': results}, 400

        return results, 200

    def list(self, payload: dict):
        db = payload['db']

        # add validation

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
        conditions = {'email': data['email']}
        data.pop('email')
        success, results = db.update_row(table_name=self.table_name, row=data, where_items=conditions)

        if not success:
            return {'error': results}, 400

        return results, 200

    def delete(self, payload: dict):
        data = payload['data']
        db = payload['db']

        # add validation

        # delete row from table
        conditions = {'email': data['email']}
        success, results = db.delete_row(table_name=self.table_name, where_items=conditions)

        if not success:
            return {'error': results}, 400

        return results, 200





