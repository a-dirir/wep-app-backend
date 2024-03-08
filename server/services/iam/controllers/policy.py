from server.database.schema import schema


class Policy:
    def __init__(self):
        self.table_name = 'iam_policies'
        self.schema = schema

    def validate_data(self, row: dict):
        # remove extra columns
        for key in row.keys():
            if key not in self.schema[self.table_name]['columns']:
                del row[key]

        for column_name, column in self.schema[self.table_name]['columns'].items():
            if column.get('not_null', False) and row.get(column_name) is None:
                return False, f'{column_name} is missing'

        return True, row

    @staticmethod
    def _expandPolicy(policy: dict):
        permissions = {}
        statements = policy['statements']

        for statement in statements:
            actions = statement['actions']
            for action in actions:
                if permissions.get(action) is None:
                    permissions[action] = {
                        statement['effect']: {
                            'customers': statement['customers'],
                            'resources': statement['resources']
                        }
                    }

                elif permissions[action].get(statement['effect']) is None:
                    permissions[action][statement['effect']] = {
                            'customers': statement['customers'],
                            'resources': statement['resources']
                    }

                else:
                    current_customers = permissions[action][statement['effect']]['customers']
                    current_resources = permissions[action][statement['effect']]['resources']

                    # add new customers to the current customers
                    for customer in statement['customers']:
                        if customer not in current_customers:
                            current_customers.append(customer)

                    # add new resources to the current resources
                    for resource in statement['resources']:
                        if resource not in current_resources:
                            current_resources.append(resource)


                    permissions[action][statement['effect']] = {
                        'customers': current_customers,
                        'resources': current_resources
                    }


        expanded_policy = {
            "version": policy['version'],
            "permissions": permissions
        }


        return expanded_policy

    def create(self, payload: dict):
        data = payload['data']
        db = payload['db']

        # validate data
        success, data = self.validate_data(data)
        if not success:
            return {'error': data}, 400

        data['expanded_policy'] = Policy._expandPolicy(data['policy'])

        # insert row into table
        success, results = db.insert_row(table_name=self.table_name, row=data)

        if not success:
            return {'error': results}, 400

        return results, 200

    def read(self, payload: dict):
        data = payload['data']
        db = payload['db']

        # validate data
        success, data = self.validate_data(data)
        if not success:
            return {'error': data}, 400

        # get row from table
        conditions = {'name': data['name']}
        success, results = db.get_row(table_name=self.table_name, where_items=conditions)

        if not success:
            return {'error': results}, 400

        return results, 200

    def list(self, payload: dict):
        db = payload['db']

        # get all rows from table
        success, results = db.get_rows(table_name=self.table_name, columns=['name', 'description', 'policy'])

        if not success:
            return {'error': results}, 400

        return results, 200

    def update(self, payload: dict):
        data = payload['data']
        db = payload['db']

        # validate data
        success, data = self.validate_data(data)
        if not success:
            return {'error': data}, 400

        data['expanded_policy'] = self._expandPolicy(data['policy'])

        # update row in table
        conditions = {'name': data['name']}
        data.pop('name')
        success, results = db.update_row(table_name=self.table_name, row=data, where_items=conditions)

        if not success:
            return {'error': results}, 400

        return results, 200

    def delete(self, payload: dict):
        data = payload['data']
        db = payload['db']

        # validate data
        success, data = self.validate_data(data)
        if not success:
            return {'error': data}, 400

        # delete row from table
        conditions = {'name': data['name']}
        success, results = db.delete_row(table_name=self.table_name, where_items=conditions)

        if not success:
            return {'error': results}, 400

        return results, 200







