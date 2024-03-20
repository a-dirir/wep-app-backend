from datetime import datetime
from server.database.schema import schema
from server.common.controller import BaseController


class SimpleCRUD(BaseController):
    def __init__(self, table_name: str):
        super().__init__()
        self.name = 'SimpleCRUD'
        self.methods = ['create', 'read', 'list', 'update', 'delete']

        self.table_name = table_name
        self.schema = schema

        self.primary_key = None
        self.foreign_keys = {}
        
        self.extract_indexes()

    def extract_indexes(self):
        for column_name, column in self.schema[self.table_name]['columns'].items():
            if column.get('primary_key', False):
                self.primary_key = column_name
            if column.get('foreign_key', False):
                foreign_table_name, foreign_column_name = column['foreign_key'].split('.')
                self.foreign_keys[column_name] = {
                    'table_name': foreign_table_name,
                    'column_name': foreign_column_name
                }

    def validate_data(self, row: dict, db):
        # remove extra columns
        new_row = {}
        for key in row.keys():
            if key in self.schema[self.table_name]['columns']:
                new_row[key] = row[key]

        row = new_row

        for column_name, column in self.schema[self.table_name]['columns'].items():
            if column.get('not_null', False) and row.get(column_name) is None:
                return False, f'{column_name} is missing'

        return True, row

    def get_foreign_keys_data(self, db):
        foreign_keys = {}
        for foreign_columns, sources in self.foreign_keys.items():
            foreign_table_name = sources['table_name']
            foreign_column_name = sources['column_name']
            success, results = db.get_rows(table_name=foreign_table_name, columns=[foreign_column_name],
                                           distinct="DISTINCT", return_type="list")

            if not success:
                return False, results

            # remove inner tuple
            results = [result[0] for result in results]
            foreign_keys[foreign_columns] = results

        return True, foreign_keys

    def create(self, payload: dict):
        data = payload['data']
        db = payload['db']

        # validate data
        success, data = self.validate_data(data, db)
        if not success:
            return {'error': data}, 400
        
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

        # validate data
        success, data = self.validate_data(data, db)
        if not success:
            return {'error': data}, 400

        conditions = {self.primary_key: data[self.primary_key]}
        del data[self.primary_key]

        # update row in table
        success, results = db.update_row(table_name=self.table_name, row=data, where_items=[conditions])
        if not success:
            return {'error': results}, 400

        return results, 200

    def delete(self, payload: dict):
        data = payload['data']
        db = payload['db']

        if data.get(self.primary_key) is None:
            return {'error': f'{self.primary_key} is missing'}, 400

        conditions = {self.primary_key: data[self.primary_key]}

        success, results = db.delete_row(table_name=self.table_name, where_items=[conditions])
        if not success:
            return {'error': results}, 400

        return results, 200
