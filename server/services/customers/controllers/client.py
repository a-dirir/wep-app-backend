from datetime import datetime
from server.database.schema import schema


class Client:
    def __init__(self, table_name: str):
        self.table_name = table_name
        self.schema = schema

        self.primary_key = None
        self.foreign_keys = {}
        
        self.extract_indexes()

    def extract_indexes(self):
        for column_name, column in self.schema['columns'].items():
            if column.get('primary_key', False):
                self.primary_key = column_name
            if column.get('foreign_key', False):
                foreign_table_name, foreign_column_name = column['foreign_key'].split('.')
                self.foreign_keys[column_name] = {
                    'table_name': foreign_table_name,
                    'column_name': foreign_column_name
                }

    def validate_row(self, row: dict, db):
        # remove extra columns
        for key in row.keys():
            if key not in self.schema['columns']:
                del row[key]

        # check if each column is valid
        for column_name, column in self.schema['columns'].items():
            if column.get('not_null', False) and row.get(column_name) is None:
                return False, f'{column_name} is missing'
            if column.get('allowed_values', False) and row.get(column_name) not in column['allowed_values']:
                return False, f'{column_name} is invalid'
            if column.get('type', False) and row.get(column_name) is not None:
                if column['type'] == 'INT' and not row[column_name].isdigit():
                    return False, f'{column_name} is invalid'
                if column['type'] == 'VARCHAR' and len(row[column_name]) > int(column['type'][8:-1]):
                    return False, f'{column_name} is invalid'
                if column['type'] == 'DATETIME':
                    try:
                        datetime.strptime(row[column_name], '%Y-%m-%d %H:%M:%S')
                    except ValueError:
                        return False, f'{column_name} is invalid'
                if column['type'] == 'DATE':
                    try:
                        datetime.strptime(row[column_name], '%Y-%m-%d')
                    except ValueError:
                        return False, f'{column_name} is invalid'
                    
            if column.get('foreign_key', False) and row.get(column_name) is not None:
                foreign_table_name = self.foreign_keys[column_name]['table_name']
                foreign_column_name = self.foreign_keys[column_name]['column_name']
                conditions = {foreign_column_name: row[column_name]}
                success, results = db.get_rows(table_name=foreign_table_name, where_items=conditions)
                if not success:
                    return False, results
                if len(results) == 0:
                    return False, f'{column_name} is invalid'
                
            if column.get('unique', False):
                conditions = {column_name: row[column_name]}
                success, results = db.get_rows(table_name=self.table_name, where_items=conditions)
                if not success:
                    return False, results
                if len(results) > 0:
                    return False, f'{column_name} is not unique'        
        
        return True, 'Row is valid'

    def get_foreign_keys_data(self, db):
        foreign_keys = {}
        for foreign_columns, sources in self.foreign_keys.items():
            foreign_table_name = sources['table_name']
            foreign_column_name = sources['column_name']
            success, results = db.get_rows(table_name=foreign_table_name, columns=[foreign_column_name], distinct="DISTINCT")
            if not success:
                return False, results
            foreign_keys[foreign_columns] = results

        return True, foreign_keys

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
        success, message = self.validate_row(data, db)
        if not success:
            return {'error': message}, 400
        
        # insert row into table
        success, results = db.insert_row(table_name=self.table_name, row=data)

        if not success:
            return {'error': results}, 400

        return results, 200

    def read(self, payload: dict):
        data = payload['data']
        db = payload['db']
        
        if data.get(self.primary_key) is None:
            return {'error': f'{self.primary_key} is missing'}, 400
        
        conditions = {self.primary_key: data[self.primary_key]}

        success, results = db.get_rows(table_name=self.table_name, where_items=conditions)
        if not success:
            return {'error': results}, 400

        return results, 200

    def list(self, payload: dict):
        db = payload['db']

        success, results = db.get_rows(table_name=self.table_name)
        if not success:
            return {'error': results}, 400

        # get foreign keys data
        success, foreign_keys_data = self.get_foreign_keys_data(db)
        if not success:
            return {'error': foreign_keys_data}, 400

        return {"rows": results, "allowed_values": foreign_keys_data}, 200

    def update(self, payload: dict):
        data = payload['data']
        db = payload['db']

        if data.get(self.primary_key) is None:
            return {'error': f'{self.primary_key} is missing'}, 400
        
        # validate row
        success, message = self.validate_row(data, db)
        if not success:
            return {'error': message}, 400

        conditions = {self.primary_key: data[self.primary_key]}
        del data[self.primary_key]

        # update row in table
        success, results = db.update_row(table_name=self.table_name, row=data, where_items=conditions)
        if not success:
            return {'error': results}, 400

        return results, 200

    def delete(self, payload: dict):
        data = payload['data']
        db = payload['db']

        if data.get(self.primary_key) is None:
            return {'error': f'{self.primary_key} is missing'}, 400

        conditions = {self.primary_key: data[self.primary_key]}

        success, results = db.delete_row(table_name=self.table_name, where_items=conditions)
        if not success:
            return {'error': results}, 400

        return results, 200
