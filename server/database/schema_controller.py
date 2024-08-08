from server.database.schema import schema


class SchemaController:
    def __init__(self):
        self.dependency_graph = self.build_dependencies_graph()

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
    def get_columns_permissions(table_name: str):
        columns_permissions = {'view': [], 'create': [], 'edit': []}

        for column_name, column in schema[table_name]['columns'].items():
            if column.get('server_only') is None:
                for permission in columns_permissions.keys():
                    columns_permissions[permission].append(column_name)
            else:
                for permission in column['server_only']:
                    if not column['server_only'][permission]:
                        columns_permissions[permission].append(column_name)

        return columns_permissions

    @staticmethod
    def remove_extra_columns(row: dict, allowed_columns: list):
        new_row = {}
        for key in row.keys():
            if key in allowed_columns:
                new_row[key] = row[key]
        return new_row

    def add_foreign_keys_aliases(self, foreign_keys: dict, records: list, db, mode="replace"):
        options = {}
        linked_columns = {}

        for foreign_column, origins in foreign_keys.items():
            table_name = origins['table_name']
            if origins['source_column_name'] != origins['destination_column_name']:
                foreign_columns_names = [origins['source_column_name'], origins['destination_column_name']]
                linked_columns[origins['source_column_name']] = f"{table_name}_{origins['destination_column_name']}"
            else:
                foreign_columns_names = [origins['source_column_name']]
                linked_columns[origins['source_column_name']] = f"{origins['source_column_name']}"

            success, results = db.get_rows(table_name=table_name, columns=foreign_columns_names,
                                           distinct="DISTINCT", return_type="list")
            if not success:
                return False, results

            options[foreign_column] = self.populate_options(results, foreign_columns_names)

        print(options, linked_columns)
        merged_records = self.merge_columns(options, linked_columns, records)

        return True, {'options': options, 'linked_columns': linked_columns, 'data': merged_records}

    @staticmethod
    def populate_options(results: list, foreign_columns_names: list):
        options = {}

        if len(results) == 0:
            return options

        if len(foreign_columns_names) == 1:
            for result in results:
                options[result[0]] = result[0]

        else:
            for result in results:
                options[result[0]] = result[1]

        return options

    @staticmethod
    def merge_columns(options, linked_columns, records: list, mode: str = "add"):
        new_records = []
        for record in records:
            new_record = record.copy()

            for foreign_column, linked_column in linked_columns.items():
                if foreign_column == linked_column:
                    continue

                source_value = record[foreign_column]
                if options[foreign_column].get(source_value) is None:
                    continue

                destination_value = options[foreign_column][source_value]

                if mode == "replace":
                    new_record[foreign_column] = destination_value

                elif mode == "add":
                    new_record[linked_column] = destination_value

            new_records.append(new_record)

        return new_records

    @staticmethod
    def remove_foreign_keys_aliases(foreign_keys: dict, record: dict, db):
        for foreign_column, origins in foreign_keys.items():
            if record.get(foreign_column) is None or origins['source_column_name'] == origins['destination_column_name']:
                continue
            else:
                # get corresponding value from source column in the database
                conditions = {origins['destination_column_name']: record[foreign_column]}
                foreign_columns_names = [origins['source_column_name'], origins['destination_column_name']]
                success, results = db.get_rows(table_name=origins['table_name'], columns=foreign_columns_names,
                                               where_items=[conditions])

                if not success:
                    return False, "Error while replacing piped foreign columns"

                record[foreign_column] = results[0][origins['source_column_name']]

        return True, record

    @staticmethod
    def build_dependency_mapping():
        dependency_mapping = {}
        for table_name, table in schema.items():
            for column_name, column in table['columns'].items():
                if column.get('foreign_key') is None:
                    dependency_mapping[f"{table_name}.{column_name}"] = None
                else:
                    dependency_mapping[f"{table_name}.{column_name}"] = column['foreign_key'].split('|')[0]

        return dependency_mapping

    def build_dependencies_graph(self):
        dependency_graph = {}
        dependency_mapping = self.build_dependency_mapping()
        for child, parent in dependency_mapping.items():
            if parent is None:
                continue

            child_table, child_column = child.split('.')
            parent_table, parent_column = parent.split('.')

            if child_table not in dependency_graph:
                dependency_graph[child_table] = {}
            if parent_table not in dependency_graph:
                dependency_graph[parent_table] = {}

            if parent_column not in dependency_graph[parent_table]:
                dependency_graph[parent_table][parent_column] = []

            if f"{child_table}" not in dependency_graph[parent_table][parent_column]:
                dependency_graph[parent_table][parent_column].append(f"{child_table}")

        return dependency_graph

    def get_dependency_graph(self, table_name: str, graph: list = None):
        if graph is None:
            graph = []

        for column_name, dependencies in self.dependency_graph[table_name].items():
            if len(dependencies) == 0:
                return graph
            else:
                graph.append([(table_name, column_name, dependency) for dependency in dependencies])
                for dependency in dependencies:
                    self.get_dependency_graph(dependency, graph)

        return graph

    def get_linked_records(self, table_name: str, data: dict, foreign_keys: dict, columns_permissions: dict, db):
        sequence = [f"{table_name}"]
        rows = {f"{table_name}": [data]}
        columns_order = {f"{table_name}": columns_permissions[table_name]['view']}
        dependency_graph = self.get_dependency_graph(table_name)

        for dependency in dependency_graph:
            for parent_table, mutual_column, child_table in dependency:
                where_items = []

                if f"{parent_table}" not in rows:
                    continue

                # fill where_items
                for row in rows[parent_table]:
                    where_items.append({mutual_column: row[mutual_column]})

                success, results = db.get_rows(child_table, where_items=where_items)

                if success and len(results) > 0:
                    rows[f"{child_table}"] = results

                    if f"{child_table}" not in sequence:
                        sequence.append(f"{child_table}")
                        columns_order[f"{child_table}"] = columns_permissions[child_table]['view']
                else:
                    continue

        for table_name in rows.keys():
            if len(foreign_keys[table_name]) != 0:
                success, results = self.add_foreign_keys_aliases(foreign_keys[table_name],
                                                                 rows[table_name], db, 'replace')
                if success:
                    rows[table_name] = results['data']

        sequence, rows, columns_order = self.format_linked_records(sequence, rows, columns_order)

        return True, {"tables_sequence": sequence, "data": rows, "columns_order": columns_order}

    @staticmethod
    def format_linked_records(sequence: list, data: dict, columns_order: dict):
        linked_records = {}
        new_columns_order = {}
        for table_name in data.keys():
            table_label = schema[table_name]['label']
            table_data = []
            for row in data[table_name]:
                new_row = {}
                for column_name in columns_order[table_name]:
                    column_label = schema[table_name]['columns'][column_name]['label']
                    new_row[column_label] = row[column_name]

                table_data.append(new_row)

            linked_records[table_label] = table_data

            new_columns_order[table_label] = [schema[table_name]['columns'][column_name]['label']
                                             for column_name in columns_order[table_name]]

        sequence = [schema[table_name]['label'] for table_name in sequence]

        return sequence, linked_records, new_columns_order
