from server.database.schema_controller_new import SchemaControllerNew
from server.util import get_logger
from server.base.controller import BaseController
from server.base.mappings import controller_db_mappings


class CRUDNew(BaseController):
    def __init__(self, name: str):
        super().__init__()
        self.name = name
        self.methods = ['create', 'list', 'update', 'delete']
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

        return True, {'data': data, 'options': options}

    def list(self, payload: dict):
        db = payload['db']

        table_name = controller_db_mappings[payload['service']][payload['controller']]

        view_columns = self.schema_controller.tables[table_name].get_view_columns()

        # get rows of table
        success, rows = db.get(table_name=table_name, columns=view_columns)
        if not success:
            return {'error': f"Error in listing {payload['controller']}"}, 400

        self.logger.info(f"Success: get rows of {table_name}")

        success, results = self.prepare_results(rows, payload)
        if not success:
            return results, 400

        return {'data': results['data'], 'options': results['options']}, 200

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

        success, data = self.on_create(input_data, db)
        if not success:
            return {'error': data}, 400

        # insert row into table
        success, results = db.insert(table_name=table_name, row=data)
        if not success:
            return {'error': results}, 400

        self.logger.info(f"Success: insert row in {table_name}")

        success, data = self.post_create(data, db)
        if not success:
            return {'error': data}, 400

        # get the newly created row
        success, data = db.get(table_name=table_name, where_items=[data])
        if not success:
            return {'error': data}, 400


        success, results = self.prepare_results([data[0]], payload)
        if not success:
            return results, 400

        return {'data': {'New Record': results['data'][0]}}, 200

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
        success, input_data = self.schema_controller.validate_input_data(table_name, input_data, 'update')
        if not success:
            return {'error': input_data}, 400

        success, data = self.on_update(input_data, db)

        # update row in table
        success, results = db.update(table_name=table_name, row=data, where_items=[condition])
        if not success:
            return {'error': results}, 400

        self.logger.info(f"Success: update row in {table_name}")

        success, data = self.post_update(data, db)

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

        success, records_to_delete = self.on_delete(records_to_delete, db)
        if not success:
            return {'error': records_to_delete}, 400

        success, results = db.delete(table_name=table_name, where_items=[condition])
        if not success:
            return {'error': results}, 400

        success, results = self.post_delete(records_to_delete, db)
        if not success:
            return {'error': results}, 400

        self.logger.info(f"Success: delete row in {table_name}")

        success, results = self.prepare_results(records_to_delete, payload)
        if not success:
            return results, 400

        return {'data': {'Deleted Records': results['data']}}, 200

    def on_create(self, data: dict, db):
        return True, data

    def post_create(self, data: dict, db):
        return True, data

    def on_update(self, data: dict, db):
        return True, data

    def post_update(self, data: dict, db):
        return True, data

    def on_delete(self, data: list, db):
        return True, data

    def post_delete(self, data: list, db):
        return True, data





