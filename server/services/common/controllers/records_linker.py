from server.base.controller import BaseController
from server.database.schema import schema
from server.database.schema_controller_new import SchemaControllerNew
from server.base.mappings import controller_db_mappings


class RecordsLinker(BaseController):
    def __init__(self):
        super().__init__()
        self.methods = ['list']
        self.dependency_graph = self.build_dependencies_graph()
        self.schema_controller = SchemaControllerNew()

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

    def list(self, payload: dict):
        db = payload['db']
        data = payload['data']

        resource = payload['access']['resource']

        if ':' not in resource:
            return {'error': 'Invalid resource'}, 400

        service, controller = resource.split(':')

        if service not in controller_db_mappings:
            return {'error': f"Service {service} not found in mappings"}, 400

        if controller not in controller_db_mappings[service]:
            return {'error': f"Controller {controller} not found in mappings"}, 400

        table_name = controller_db_mappings[service][controller]

        view_columns = self.schema_controller.tables[table_name].get_view_columns()

        # ensure client supplied required fields for index data used for update
        index_data = data.get('index_data')
        success, condition = self.schema_controller.validate_index_data(table_name, index_data)
        if not success:
            return {'error': condition}, 400

        # get rows of table
        success, rows = db.get(table_name=table_name, columns=view_columns, where_items=[condition])
        if not success:
            return {'error': f"Error in listing {payload['controller']}"}, 400

        sequence = [f"{table_name}"]
        rows = {f"{table_name}": rows}
        columns_order = {f"{table_name}": view_columns}
        dependency_graph = self.get_dependency_graph(table_name)

        for dependency in dependency_graph:
            for parent_table, mutual_column, child_table in dependency:
                where_items = []

                if f"{parent_table}" not in rows:
                    continue

                # fill where_items
                for row in rows[parent_table]:
                    where_items.append({mutual_column: row[mutual_column]})

                success, results = db.get(child_table, where_items=where_items)

                if success and len(results) > 0:
                    rows[f"{child_table}"] = results

                    if f"{child_table}" not in sequence:
                        sequence.append(f"{child_table}")
                        columns_order[f"{child_table}"] = self.schema_controller.tables[child_table].get_view_columns()
                else:
                    continue

        sequence, rows, columns_order = self.format_linked_records(sequence, rows, columns_order)

        return {"tables_sequence": sequence, "data": rows, "columns_order": columns_order}, 200

