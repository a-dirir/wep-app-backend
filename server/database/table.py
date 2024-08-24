# foreign_keys_config format: {
#     foreign_column: {
#         table_name: table_name,
#         source_column_name: source_column_name,
#         destination_column_name: destination_column_name
#     }
# }


class Table:
    def __init__(self, table_schema: dict):
        self.table_schema = table_schema
        self.index_columns = []
        self.view_columns = []
        self.foreign_columns = {}

        self.set()

    def set(self):
        self.set_index_columns()
        self.set_view_columns()
        self.set_foreign_columns()

    def set_index_columns(self):
        self.index_columns = []
        for column_name, column_properties in self.table_schema['columns'].items():
            if column_properties.get('index') is not None or column_properties.get('index') is not False:
                self.index_columns.append(column_name)

    def set_view_columns(self):
        self.view_columns = []
        for column_name, column_properties in self.table_schema['columns'].items():
            if column_properties.get('client_permission') is None:
                self.view_columns.append(column_name)
            elif column_properties['client_permission']['view'] is True:
                self.view_columns.append(column_name)

    def set_foreign_columns(self):
        self.foreign_columns = {}
        for column_name, column_properties in self.table_schema['columns'].items():
            if column_properties.get('foreign_key', False):
                if column_properties['foreign_key'].find('|') != -1:
                    source, destination = column_properties['foreign_key'].split('|')
                    source_table_name, source_column_name = source.split('.')
                    destination_table_name, destination_column_name = destination.split('.')
                else:
                    source_table_name, source_column_name = column_properties['foreign_key'].split('.')
                    destination_table_name, destination_column_name = source_table_name, source_column_name

                foreign_key_alias = column_properties.get('foreign_key_alias',
                                                          f"{source_table_name}_{destination_column_name}")

                self.foreign_columns[column_name] = {
                    'table_name': source_table_name,
                    'source_column_name': source_column_name,
                    'destination_column_name': destination_column_name,
                    'foreign_key_alias': foreign_key_alias
                }

    def get_index_columns(self):
        return self.index_columns

    def get_view_columns(self):
        return self.view_columns

    def get_foreign_columns(self):
        return self.foreign_columns

    def get_required_and_optional_columns(self, mode: str = 'create'):
        required_columns = []
        optional_columns = []

        for column_name, column_properties in self.table_schema['columns'].items():
            if column_name in self.foreign_columns:
                required_columns.append(column_name)
                continue

            if column_properties.get('required') is None or column_properties.get('required') is True:
                if column_properties.get('client_permission') is None:
                    required_columns.append(column_name)
                elif column_properties['client_permission'][mode] is True:
                    required_columns.append(column_name)
            else:
                if column_properties.get('client_permission') is None and column_name not in required_columns:
                    optional_columns.append(column_name)
                elif column_properties['client_permission'][mode] is True and column_name not in required_columns:
                    optional_columns.append(column_name)

        return required_columns, optional_columns

    def get_labels(self,):
        labels = {}
        for column_name in self.table_schema['columns']:
            labels[column_name] = self.table_schema['columns'][column_name]['label']

        return labels

    def get_column_names_from_labels(self, labels: list):
        column_names = []
        for label in labels:
            for column_name, column_properties in self.table_schema['columns'].items():
                if column_properties['label'] == label:
                    column_names.append(column_name)
                    break

        return column_names

    def get_column_order(self):
        return self.table_schema['column_order']

    def get_form_config(self):
        view_columns = self.get_view_columns()
        form_config = {}

        for column_name, column_properties in self.table_schema['columns'].items():
            if column_name not in view_columns:
                continue

            form_config[column_properties['label']] = {
                'type': column_properties['type'],
                'permission': column_properties.get('client_permission', {'create': False,
                                                                          'edit': False, 'view': True}),
            }

        return form_config
