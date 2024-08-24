from server.database.schema_controller_new import SchemaControllerNew
from server.util import get_logger
from server.database.schema import schema
from server.common.controller import BaseController
from server.database.schema_controller import SchemaController
from server.common.mappings import controller_db_mappings


class CRUDNew(BaseController):
    def __init__(self, name: str):
        super().__init__()
        self.name = name
        self.methods = ['create', 'list', 'update', 'delete', 'showLinkedServices']
        self.logger = get_logger(f"CRUD_{name}")

        self.schema_controller = SchemaControllerNew()

    def prepare_results(self, results: list, payload: dict):
        db = payload['db']

        table_name = controller_db_mappings[payload['service']][payload['controller']]

        if len(results) > 3:
            records = None
        elif 0 < len(results) <= 3:
            records = results
        else:
            return False, {'error': f"No data found for {payload['controller']}"}

        # get foreign columns unique values
        success, foreign_columns_data = self.schema_controller.get_foreign_columns_data(table_name, db, records)
        if not success:
            return {'error': f"Error in listing {payload['controller']}"}, 400

        # join foreign columns unique values with rows
        data, options = self.schema_controller.join_records_and_foreign_columns(results, foreign_columns_data)

        data = self.schema_controller.replace_column_name_with_label(table_name, data)
        options = self.schema_controller.replace_column_name_with_label(table_name, [options])

        return True, {'data': data, 'options': options[0]}

    def list(self, payload: dict):
        db = payload['db']

        table_name = controller_db_mappings[payload['service']][payload['controller']]

        # get rows of table
        success, rows = db.get(table_name=table_name)
        if not success:
            return {'error': f"Error in listing {payload['controller']}"}, 400

        self.logger.info(f"Success: get rows of {table_name}")

        success, results = self.prepare_results(rows, payload)
        if not success:
            return results, 400

        form_config, column_order = self.schema_controller.get_table_config(table_name)

        return {'data': results['data'], 'options': results['options'],
                'form_config': form_config, 'column_order': column_order}, 200

    def create(self, payload: dict):
        data = payload['data']
        db = payload['db']

        if data is None or len(data) == 0:
            return {'error': 'No data to create'}, 400

        table_name = controller_db_mappings[payload['service']][payload['controller']]

        # ensure client supplied required fields
        input_data = data.get('input_data')
        success, input_data = self.schema_controller.validate_input_data(table_name, input_data)
        if not success:
            return {'error': input_data}, 400

        data = self.on_create(input_data, db)

        # insert row into table
        success, results = db.insert(table_name=table_name, row=data)
        if not success:
            return {'error': results}, 400

        self.logger.info(f"Success: insert row in {table_name}")

        success, results = self.prepare_results([data], payload)
        if not success:
            return results, 400

        return {'data': {'New Record': results['data']}}, 200

    def update(self, payload: dict):
        data = payload['data']
        db = payload['db']

        if data is None or len(data) == 0:
            return {'error': 'No data to update'}, 400

        table_name = controller_db_mappings[payload['service']][payload['controller']]

        # ensure client supplied required fields for index data used for update
        index_data = data.get('index_data')
        success, condition = self.schema_controller.validate_index_data(table_name, index_data)
        if not success:
            return {'error': condition}, 400

        # check if there are data to update in the table
        success, old_records = db.get(table_name=table_name, where_items=[condition])
        if not success:
            return {'error': old_records}, 400
        elif len(old_records) == 0:
            return {'error': 'No record found to update'}, 400

        # ensure client supplied required fields for input data used for update
        input_data = data.get('input_data')
        success, input_data = self.schema_controller.validate_input_data(table_name, input_data, 'edit')
        if not success:
            return {'error': input_data}, 400

        data = self.on_update(input_data, db)

        # update row in table
        success, results = db.update(table_name=table_name, row=data, where_items=[condition])
        if not success:
            return {'error': results}, 400

        self.logger.info(f"Success: update row in {table_name}")

        # combine condition and input data to get updated row
        for key, value in condition.items():
            if key not in data:
                data[key] = value

        success, results = self.prepare_results([old_records[0], data], payload)
        if not success:
            return results, 400

        return {'data': {'Old Record': results['data'][0], 'New Record': results['data'][1]}}, 200

    def delete(self, payload: dict):
        data = payload['data']
        db = payload['db']

        if data is None or len(data) == 0:
            return {'error': 'No data to delete'}, 400

        table_name = controller_db_mappings[payload['service']][payload['controller']]

        # ensure client supplied required fields for index data used for update
        index_data = data.get('index_data')
        success, condition = self.schema_controller.validate_index_data(table_name, index_data)
        if not success:
            return {'error': condition}, 400

        # check if there are data to delete in the table
        success, records_to_delete = db.get(table_name=table_name, where_items=[condition])
        if not success:
            return {'error': records_to_delete}, 400
        elif len(records_to_delete) == 0:
            return {'error': 'No record found to delete'}, 400

        success, results = db.delete(table_name=table_name, where_items=[condition])
        if not success:
            return {'error': results}, 400

        self.logger.info(f"Success: delete row in {table_name}")

        success, results = self.prepare_results(records_to_delete, payload)
        if not success:
            return results, 400

        return {'data': {'Deleted Records': results['data']}}, 200

    def on_create(self, data: dict, db):
        return data

    def on_update(self, data: dict, db):
        return data





