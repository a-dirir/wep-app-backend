from server.database.schema import schema


class SchemaController:
    def __init__(self):
        self.dependency_graph = self.build_dependencies_graph()

    @staticmethod
    def extract_indexes(table_name: str):
        index_keys = []
        foreign_keys = {}
        for column_name, column in schema[table_name]['columns'].items():
            if column.get('index', False):
                index_keys.append(column_name)

            if column.get('foreign_key', False):
                if column['foreign_key'].find('=>') != -1:
                    source, destination = column['foreign_key'].split('=>')
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

        return index_keys, foreign_keys

    @staticmethod
    def get_client_side_columns(table_name: str):
        get_client_side_columns = []

        for column_name, column in schema[table_name]['columns'].items():
            if not column.get('server_only', False):
                get_client_side_columns.append(column_name)

        return get_client_side_columns

    def replace_source_with_destination(self, foreign_keys_config: dict, records: list, db):
        columns_distinct_values = {}
        for foreign_column, origins in foreign_keys_config.items():
            table_name = origins['table_name']
            foreign_columns_names = [origins['destination_column_name']]

            if origins['source_column_name'] != origins['destination_column_name']:
                foreign_columns_names.append(origins['source_column_name'])

            success, results = db.get_rows(table_name=table_name, columns=foreign_columns_names,
                                           distinct="DISTINCT", return_type="list")
            if not success:
                return False, results

            columns_distinct_values[foreign_column] = results

        columns_distinct_values, data = self.merge_columns(columns_distinct_values, records)

        return True, {'options': columns_distinct_values, 'data': records}

    @staticmethod
    def merge_columns(columns_distinct_values, records: list):
        for column_name, column_values in columns_distinct_values.items():
            if len(column_values[0]) > 1:
                for row in records:
                    # replace foreign key with value
                    row[column_name] = [item[0] for item in column_values if item[1] == row[column_name]][0]

            columns_distinct_values[column_name] = [item[0] for item in column_values]

        return columns_distinct_values, records

    @staticmethod
    def replace_destination_with_source(foreign_keys_config: dict, record: dict, db):
        for foreign_column, origins in foreign_keys_config.items():
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
                    dependency_mapping[f"{table_name}.{column_name}"] = column['foreign_key'].split('=>')[0]

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

    def get_linked_records(self, table_name: str, data: dict, db):
        sequence = [f"{table_name}"]
        rows = {f"{table_name}": [data]}

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
                else:
                    continue
        return True, {"sequence": sequence, "linked_records": rows}
