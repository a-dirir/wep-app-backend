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
        self.columns_permissions = {}

        self.load_table_metadata()

    def load_table_metadata(self):
        for table_name in self.schema.keys():
            self.index_keys[table_name] = self.schema_controller.get_index_keys(table_name)
            self.foreign_keys[table_name] = self.schema_controller.get_foreign_keys(table_name)
            self.columns_permissions[table_name] = self.schema_controller.get_columns_permissions(table_name)

    def validate_data(self, table_name: str, row: dict):
        for column_name, column in self.schema[table_name]['columns'].items():
            if column.get('not_null', False) and row.get(column_name) is None:
                return False, f'{column_name} is missing'

        return True, row

    def list(self, payload: dict):
        db = payload['db']

        table_name = controller_db_mappings[payload['service']][payload['controller']]
        view_columns = self.columns_permissions[table_name]['view']

        success, results = db.get_rows(table_name=table_name, columns=view_columns)
        if not success:
            return {'error': f"Error in listing {payload['controller']}"}, 400
        self.logger.info(f"Success: list {table_name}")

        # get foreign keys data
        success, results = self.schema_controller.add_foreign_keys_aliases(self.foreign_keys[table_name],
                                                                           results, db)
        if not success:
            return {'error': results}, 400
        self.logger.info(f"Success: replace source with destination in {table_name}")

        return results, 200

    def create(self, payload: dict):
        data = payload['data']
        db = payload['db']

        table_name = controller_db_mappings[payload['service']][payload['controller']]

        data = self.schema_controller.remove_extra_columns(data, self.columns_permissions[table_name]['create'])
        if data is None or len(data) == 0:
            return {'error': 'No data to insert'}, 400

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

        results = [{col: data[col] for col in self.columns_permissions[table_name]['view']}]

        return {'data': results}, 200

    def prepare_update_data(self, table_name: str, data: dict):
        if data.get('new') is None or data.get('old') is None:
            return False, 'new and old data are required'

        data['new'] = self.schema_controller.remove_extra_columns(data['new'],
                                                                  self.columns_permissions[table_name]['view'])
        data['old'] = self.schema_controller.remove_extra_columns(data['old'],
                                                                  self.columns_permissions[table_name]['view'])

        if data['new'] is None or len(data['new']) == 0:
            return False, 'No new data to update'

        if data['old'] is None or len(data['old']) == 0:
            return False, 'No old data to update'

        for key in self.index_keys[table_name]:
            if data['old'].get(key) is None:
                return False, f'{key} is missing in old data'

        conditions = {key: data['old'][key] for key in self.index_keys[table_name]}

        return True, {'conditions': conditions, 'data': data['new']}

    def update(self, payload: dict):
        data = payload['data']
        db = payload['db']

        table_name = controller_db_mappings[payload['service']][payload['controller']]

        success, result = self.prepare_update_data(table_name, data)
        if not success:
            return {'error': result}, 400

        conditions = result['conditions']
        data = result['data']

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

        results = [{col: data[col] for col in self.columns_permissions[table_name]['view']}]

        return {'data': results}, 200

    def delete(self, payload: dict):
        data = payload['data']
        db = payload['db']

        if data is None or len(data) == 0:
            return {'error': 'No data to delete'}, 400

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

    def on_create(self, data: dict, db):
        return data

    def on_update(self, data: dict, db):
        return data

    def showLinkedServices(self, payload: dict):
        data = payload['data']
        db = payload['db']

        if data is None or len(data) == 0:
            return {'error': 'No data to show Linked Services for..'}, 400

        table_name = controller_db_mappings[payload['service']][payload['controller']]

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
                                                                     self.columns_permissions, db)
        if not success:
            return {'error': results}, 400

        self.logger.info(f"Success: get linked records in {table_name}")

        return results, 200
