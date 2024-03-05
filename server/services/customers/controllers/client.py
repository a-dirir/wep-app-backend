from datetime import datetime
from server.database.schema import schema
from server.database.simple_crud import SimpleCRUD


class Client(SimpleCRUD):
    def __init__(self, table_name: str):
        super().__init__(table_name)
        self.primary_key = None
        self.foreign_keys = {}
        self.extract_indexes()

    def create(self, payload: dict):
        data = payload['data']
        db = payload['db']

        # check if Name is missing
        if data.get('Name') is None:
            return {'error': 'Name is missing'}, 400

        # check if Name is at least 5 characters long
        if len(data['Name']) < 5:
            return {'error': 'Name is too short'}, 400

        # generate Client_ID from by getting first 5 letters from and Name, - and last 4 letters from the Name
        data[self.primary_key] = data['Name'][:5] + '-' + data['Name'][-4:]

        # validate row
        # success, message = self.validate_row(data, db)
        # if not success:
        #     return {'error': message}, 400
        
        # insert row into table
        success, results = db.insert_row(table_name=self.table_name, row=data)

        if not success:
            return {'error': results}, 400

        return results, 200

    def update(self, payload: dict):
        data = payload['data']
        db = payload['db']

        if data.get(self.primary_key) is None:
            return {'error': f'{self.primary_key} is missing'}, 400
        
        # validate row
        # success, message = self.validate_row(data, db)
        # if not success:
        #     return {'error': message}, 400

        conditions = {self.primary_key: data[self.primary_key]}
        del data[self.primary_key]

        # update row in table
        success, results = db.update_row(table_name=self.table_name, row=data, where_items=conditions)
        if not success:
            return {'error': results}, 400

        return results, 200
