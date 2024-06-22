from server.database.schema import schema
from server.common.controller import BaseController
from server.database.schema_controller import SchemaController


class SimpleCRUD(BaseController):
    def __init__(self, table_name: str):
        super().__init__()
        self.name = 'SimpleCRUD'
        self.methods = ['create', 'list', 'update', 'delete', 'showLinkedServices']

        self.table_name = table_name
        self.schema = schema
        self.schema_controller = SchemaController()

        self.index_keys, self.foreign_keys = self.schema_controller.extract_indexes(self.table_name)
        self.client_side_columns = self.schema_controller.get_client_side_columns(self.table_name)

    def remove_extra_columns(self, row: dict):
        new_row = {}
        for key in row.keys():
            if key in self.schema[self.table_name]['columns']:
                new_row[key] = row[key]
        return new_row

    def validate_data(self, row: dict):
        for column_name, column in self.schema[self.table_name]['columns'].items():
            if column.get('not_null', False) and row.get(column_name) is None and not column.get('server_only', False):
                return False, f'{column_name} is missing'

        return True, row

    def list(self, payload: dict):
        db = payload['db']

        success, results = db.get_rows(table_name=self.table_name, columns=self.client_side_columns)
        if not success:
            return {'error': results}, 400
        self.logger.info(f"Success: list rows in {self.table_name}")

        # get foreign keys data
        success, data = self.schema_controller.replace_source_with_destination(self.foreign_keys, results, db)
        if not success:
            return {'error': data}, 400
        self.logger.info(f"Success: replace source with destination in {self.table_name}")

        return data, 200

    def create(self, payload: dict):
        data = payload['data']
        db = payload['db']

        data = self.remove_extra_columns(data)

        success, data = self.schema_controller.replace_destination_with_source(self.foreign_keys, data, db)
        if not success:
            return {'error': data}, 400
        self.logger.info(f"Success: replace destination with source in {self.table_name} for create")

        data = self.on_create(data, db)

        # validate data
        success, data = self.validate_data(data)
        if not success:
            return {'error': data}, 400

        # insert row into table
        success, results = db.insert_row(table_name=self.table_name, row=data)
        if not success:
            return {'error': results}, 400
        self.logger.info(f"Success: insert row in {self.table_name}")

        return results, 200

    def update(self, payload: dict):
        data = payload['data']
        db = payload['db']

        data['new'] = self.remove_extra_columns(data['new'])
        data['old'] = self.remove_extra_columns(data['old'])

        for key in self.index_keys:
            if data['old'].get(key) is None:
                return {'error': f'{key} is missing'}, 400

        conditions = {key: data['old'][key] for key in self.index_keys}

        data = data['new']

        success, data = self.schema_controller.replace_destination_with_source(self.foreign_keys, data, db)
        if not success:
            return {'error': data}, 400
        self.logger.info(f"Success: replace destination with source in {self.table_name} for update")

        data = self.on_update(data, db)

        # validate data
        success, data = self.validate_data(data)
        if not success:
            return {'error': data}, 400

        # update row in table
        success, results = db.update_row(table_name=self.table_name, row=data, where_items=[conditions])
        if not success:
            return {'error': results}, 400
        self.logger.info(f"Success: update row in {self.table_name}")

        return results, 200

    def delete(self, payload: dict):
        data = payload['data']
        db = payload['db']

        for key in self.index_keys:
            if data.get(key) is None:
                return {'error': f'{key} is missing'}, 400

        conditions = {key: data[key] for key in self.index_keys}

        success, results = db.delete_row(table_name=self.table_name, where_items=[conditions])
        if not success:
            return {'error': results}, 400
        self.logger.info(f"Success: delete row in {self.table_name}")

        return results, 200

    def on_create(self, data: dict, db):
        return data

    def on_update(self, data: dict, db):
        return data

    def showLinkedServices(self, payload: dict):
        data = payload['data']
        db = payload['db']

        success, data = self.schema_controller.replace_destination_with_source(self.foreign_keys, data, db)
        if not success:
            return {'error': data}, 400

        for key in self.index_keys:
            if data.get(key) is None:
                return {'error': f'{key} is missing'}, 400

        conditions = {key: data[key] for key in self.index_keys}

        # get full row
        success, results = db.get_rows(table_name=self.table_name, where_items=[conditions])
        if not success:
            return {'error': results}, 400

        updated_data = results[0]
        # get linked records
        success, results = self.schema_controller.get_linked_records(self.table_name, updated_data, db)

        if not success:
            return {'error': results}, 400

        return results, 200
