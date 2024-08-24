from server.database.schema import schema
from server.database.table import Table


class SchemaControllerNew:
    def __init__(self):
        self.tables = {}
        self.set()

    def set(self):
        for table_name in schema.keys():
            self.tables[table_name] = Table(schema[table_name])

    @staticmethod
    def format_foreign_columns_data(results: list, foreign_columns_names: list):
        options = {}
        if len(results) == 0:
            return options

        source_column_name = foreign_columns_names[0]

        if len(foreign_columns_names) == 1:
            for result in results:
                options[result[source_column_name]] = result[source_column_name]
        else:
            destination_column_name = foreign_columns_names[1]
            for result in results:
                options[result[source_column_name]] = result[destination_column_name]

        return options

    def get_foreign_columns_data(self, table_name: str, db, records: list = None):
        foreign_columns_data = {}

        foreign_columns = self.tables[table_name].get_foreign_columns()

        for foreign_column_name, config in foreign_columns.items():
            table_name = config['table_name']
            if config['source_column_name'] != config['destination_column_name']:
                columns_returned = [config['source_column_name'], config['destination_column_name']]
            else:
                columns_returned = [config['source_column_name']]

            if records is not None:
                condition = []
                for record in records:
                    if record[config['source_column_name']] is not None:
                        condition.append({config['source_column_name']: record[config['source_column_name']]})
            else:
                condition = None

            success, unique_values = db.get(table_name=table_name, columns=columns_returned,
                                            distinct="DISTINCT", where_items=condition)

            if not success:
                return False, unique_values

            foreign_columns_data[foreign_column_name] = {
                'source_column': config['source_column_name'],
                'destination_column': config['destination_column_name'],
                'foreign_key_alias': config['foreign_key_alias'],
                'unique_values': self.format_foreign_columns_data(unique_values, columns_returned),
            }

        return True, foreign_columns_data

    @staticmethod
    def join_records_and_foreign_columns(records: list, foreign_columns_data: dict):
        foreign_columns = {}

        for foreign_column_name, foreign_column_config in foreign_columns_data.items():
            source_column_name = foreign_column_config['source_column']
            destination_column_name = foreign_column_config['destination_column']
            foreign_key_alias = foreign_column_config['foreign_key_alias']
            unique_values = foreign_column_config['unique_values']

            for index, record in enumerate(records):

                if source_column_name == destination_column_name:
                    continue

                source_value = record[source_column_name]
                if unique_values.get(source_value) is None:
                    records[index][foreign_key_alias] = ""
                    continue

                destination_value = unique_values.get(source_value)
                if destination_value is None:
                    records[index][foreign_key_alias] = ""
                else:
                    records[index][foreign_key_alias] = destination_value

            foreign_columns[foreign_column_name] = unique_values

        return records, foreign_columns

    def validate_index_data(self, table_name: str, data: dict):
        if data is None or len(data) == 0:
            return False, 'No data provided'

        index_columns = self.tables[table_name].get_index_columns()
        index_data = {}

        for column_name in index_columns:
            if data.get(column_name) is None:
                return False, f'{column_name} is missing'

            index_data[column_name] = data[column_name]

        return True, index_data

    def validate_input_data(self, table_name: str, data: dict, mode: str = 'create'):
        if data is None or len(data) == 0:
            return False, 'No data provided'

        required_columns, optional_columns = self.tables[table_name].get_required_and_optional_columns(mode)
        validated_data = {}

        for column_name in required_columns:
            if data.get(column_name) is None:
                return False, f'{column_name} is missing'
            validated_data[column_name] = data[column_name]

        for column_name in optional_columns:
            if data.get(column_name) is not None:
                validated_data[column_name] = data[column_name]

        return True, validated_data

    def replace_column_name_with_label(self, table_name: str, records: list):
        labels = self.tables[table_name].get_labels()
        view_columns = self.tables[table_name].get_view_columns()
        new_records = []

        for record in records:
            new_record = {}
            for column_name, column_value in record.items():
                if labels.get(column_name) is not None:
                    if column_name in view_columns:
                        new_record[labels[column_name]] = column_value
                else:
                    new_record[column_name] = column_value

            new_records.append(new_record)

        return new_records

    def get_table_config(self, table_name: str):
        form_config = self.tables[table_name].get_form_config()

        column_order = self.tables[table_name].get_column_order()

        return form_config, column_order

