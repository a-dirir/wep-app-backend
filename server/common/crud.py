from server.util import get_logger
from server.database.schema import schema
from server.common.controller import BaseController
from server.database.schema_controller import SchemaController
from server.common.mappings import controller_db_mappings


class CRUD(BaseController):
    def __init__(self, name: str):
        super().__init__()
        self.name = name
        self.methods = ['create', 'list', 'update', 'delete', 'showLinkedServices']
        self.logger = get_logger(f"CRUD_{name}")

        self.schema = schema
        self.schema_controller = SchemaController()

        self.index_keys = {}
        self.foreign_keys = {}
        self.client_side_columns = {}

        self.load_table_metadata()

    def load_table_metadata(self):
        for table_name in self.schema.keys():
            self.index_keys[table_name] = self.get_index_keys(table_name)
            self.foreign_keys[table_name] = self.get_foreign_keys(table_name)
            self.client_side_columns[table_name] = self.get_client_side_columns(table_name)

    @staticmethod
    def get_index_keys(table_name: str):
        index_keys = []
        for column_name, column in schema[table_name]['columns'].items():
            if column.get('index', False):
                index_keys.append(column_name)

        return index_keys

    @staticmethod
    def get_foreign_keys(table_name: str):
        foreign_keys = {}
        for column_name, column in schema[table_name]['columns'].items():
            if column.get('foreign_key', False):
                if column['foreign_key'].find('|') != -1:
                    source, destination = column['foreign_key'].split('|')
                    source_table_name, source_column_name = source.split('.')
                    destination_table_name, destination_column_name = destination.split('.')
                else:
                    source_table_name, source_column_name = column['foreign_key'].split('.')
                    destination_table_name, destination_column_name = source_table_name, source_column_name

                foreign_keys[column_name] = {
                    'table_name': source_table_name,
                    'source_column_name': source_column_name,
                    'destination_column_name': destination_column_name
                }

        return foreign_keys

    @staticmethod
    def get_client_side_columns(table_name: str):
        get_client_side_columns = []

        for column_name, column in schema[table_name]['columns'].items():
            if not column.get('server_only', False):
                get_client_side_columns.append(column_name)

        return get_client_side_columns

    def remove_extra_columns(self, table_name: str, row: dict):
        new_row = {}
        for key in row.keys():
            if key in self.schema[table_name]['columns']:
                new_row[key] = row[key]
        return new_row

    def validate_data(self, table_name: str, row: dict):
        for column_name, column in self.schema[table_name]['columns'].items():
            if column.get('not_null', False) and row.get(column_name) is None and not column.get('server_only', False):
                return False, f'{column_name} is missing'

        return True, row

    def list(self, payload: dict):
        db = payload['db']

        table_name = controller_db_mappings[payload['service']][payload['controller']]

        success, results = db.get_rows(table_name=table_name, columns=self.client_side_columns[table_name])
        if not success:
            return {'error': results}, 400
        self.logger.info(f"Success: list rows in {table_name}")

        # get foreign keys data
        success, results = self.schema_controller.replace_source_with_destination(self.foreign_keys[table_name],
                                                                                  results, db)
        if not success:
            return {'error': results}, 400
        self.logger.info(f"Success: replace source with destination in {table_name}")

        return results, 200

    def create(self, payload: dict):
        data = payload['data']
        db = payload['db']

        table_name = controller_db_mappings[payload['service']][payload['controller']]

        data = self.remove_extra_columns(table_name, data)

        success, data = self.schema_controller.replace_destination_with_source(self.foreign_keys[table_name], data, db)
        if not success:
            return {'error': data}, 400
        self.logger.info(f"Success: replace destination with source in {table_name} for create")

        data = self.on_create(data, db)

        # validate data
        success, data = self.validate_data(table_name, data)
        if not success:
            return {'error': data}, 400

        # insert row into table
        success, results = db.insert_row(table_name=table_name, row=data)
        if not success:
            return {'error': results}, 400
        self.logger.info(f"Success: insert row in {table_name}")

        return results, 200

    def update(self, payload: dict):
        data = payload['data']
        db = payload['db']

        table_name = controller_db_mappings[payload['service']][payload['controller']]

        data['new'] = self.remove_extra_columns(table_name, data['new'])
        data['old'] = self.remove_extra_columns(table_name, data['old'])

        for key in self.index_keys[table_name]:
            if data['old'].get(key) is None:
                return {'error': f'{key} is missing'}, 400

        conditions = {key: data['old'][key] for key in self.index_keys[table_name]}

        data = data['new']

        success, data = self.schema_controller.replace_destination_with_source(self.foreign_keys[table_name], data, db)
        if not success:
            return {'error': data}, 400
        self.logger.info(f"Success: replace destination with source in {table_name} for update")

        data = self.on_update(data, db)

        # validate data
        success, data = self.validate_data(table_name, data)
        if not success:
            return {'error': data}, 400

        # update row in table
        success, results = db.update_row(table_name=table_name, row=data, where_items=[conditions])
        if not success:
            return {'error': results}, 400
        self.logger.info(f"Success: update row in {table_name}")

        return results, 200

    def delete(self, payload: dict):
        data = payload['data']
        db = payload['db']

        table_name = controller_db_mappings[payload['service']][payload['controller']]

        for key in self.index_keys[table_name]:
            if data.get(key) is None:
                return {'error': f'{key} is missing'}, 400

        conditions = {key: data[key] for key in self.index_keys[table_name]}

        success, results = db.delete_row(table_name=table_name, where_items=[conditions])
        if not success:
            return {'error': results}, 400
        self.logger.info(f"Success: delete row in {table_name}")

        return results, 200

    @staticmethod
    def on_create(data: dict, db):
        return data

    @staticmethod
    def on_update(data: dict, db):
        return data

    def showLinkedServices(self, payload: dict):
        data = payload['data']
        db = payload['db']

        table_name = controller_db_mappings[payload['service']][payload['controller']]

        success, data = self.schema_controller.replace_destination_with_source(self.foreign_keys[table_name], data, db)
        if not success:
            return {'error': data}, 400
        self.logger.info(f"Success: replace destination with source in {table_name} for showLinkedServices")

        for key in self.index_keys[table_name]:
            if data.get(key) is None:
                return {'error': f'{key} is missing'}, 400

        conditions = {key: data[key] for key in self.index_keys[table_name]}

        # get full row
        success, results = db.get_rows(table_name=table_name, where_items=[conditions])
        if not success:
            return {'error': results}, 400

        updated_data = results[0]

        # get linked records
        success, results = self.schema_controller.get_linked_records(table_name, updated_data, self.foreign_keys,
                                                                     self.client_side_columns, db)
        if not success:
            return {'error': results}, 400
        self.logger.info(f"Success: get linked records in {table_name}")

        return results, 200
