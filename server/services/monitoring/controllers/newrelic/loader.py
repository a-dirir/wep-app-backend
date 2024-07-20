from server.services.monitoring.controllers.newrelic.agent import NewRelicAgent


class NewRelicLoader:
    def __init__(self):
        self.agent = NewRelicAgent()

    def LoadAccounts(self, payload: dict):
        db = payload['db']

        success, results = db.get_rows(table_name='newrelic_organizations', columns=['Organization_ID'],
                                       return_type='list')
        if not success:
            return results, 400

        db_accounts = [result[0] for result in results]

        newrelic_accounts = self.agent.get_accounts()
        if newrelic_accounts is None:
            return 'Failed to get newrelic accounts', 400

        # check if there are any new accounts
        for newrelic_account in newrelic_accounts:
            if str(newrelic_account['id']) not in db_accounts:
                new_organization = {
                    'Organization_ID': newrelic_account['id'],
                    'Organization_NAME': newrelic_account['name'],
                    'Sub_Client_ID': 'Bespi-Root'
                }

                success, results = db.insert_row(table_name='newrelic_organizations', row=new_organization)
                if not success:
                    return False, results

        return 'Loaded newrelic accounts successfully', 200

    def LoadAlertPolicies(self, payload: dict):
        db = payload['db']

        account_id = payload['data']['account_id']

        success, results = db.get_rows(table_name='newrelic_alerts_policies', columns=['Alert_Policy_ID'],
                                       return_type='list', where_items=[{'Organization_ID': account_id}])
        if not success:
            return results, 400

        db_policies = [result[0] for result in results]

        newrelic_policies = self.agent.get_policies(account_id)
        if newrelic_policies is None:
            return 'Failed to get alert policies', 400

        # check if there are any new policies
        for newrelic_policy in newrelic_policies:
            if newrelic_policy['id'] not in db_policies:
                new_policy = {
                    'Organization_ID': account_id,
                    'Alert_Policy_ID': newrelic_policy['id'],
                    'Alert_Policy_NAME': newrelic_policy['name']
                }

                success, results = db.insert_row(table_name='newrelic_alerts_policies', row=new_policy)
                if not success:
                    return False, results

        return 'Loaded newrelic alert policies successfully', 200

    def LoadAlertConditions(self, payload: dict):
        db = payload['db']

        account_id = payload['data']['account_id']
        policy_id = payload['data']['policy_id']

        success, results = db.get_rows(table_name='newrelic_alerts_conditions', columns=['Condition_ID'],
                                       return_type='list', where_items=[{'Alert_Policy_ID': policy_id}])
        if not success:
            return results, 400

        db_conditions = [result[0] for result in results]

        newrelic_conditions = self.agent.get_all_alerts_conditions(account_id, policy_id)
        if newrelic_conditions is None:
            return 'Failed to get alert conditions', 400

        # check if there are any new conditions
        for newrelic_condition in newrelic_conditions:
            if newrelic_condition['id'] not in db_conditions:
                new_condition = {
                    'Alert_Policy_ID': policy_id,
                    'Condition_ID': newrelic_condition['id'],
                    'Condition_NAME': newrelic_condition['name'],
                    'Condition_Query': newrelic_condition['nrql']['query'],

                }

                condition_details = self.agent.get_alert_condition_details(account_id, newrelic_condition['id'])
                if condition_details is None:
                    return 'Failed to get alert condition details', 400

                new_condition['Condition_Operator'] = condition_details['terms'][0]['operator']
                new_condition['Condition_Threshold'] = condition_details['terms'][0]['threshold']
                new_condition['Condition_Threshold_Duration'] = condition_details['terms'][0]['thresholdDuration']

                success, results = db.insert_row(table_name='newrelic_alerts_conditions', row=new_condition)
                if not success:
                    return False, results

        return 'Loaded newrelic alert conditions successfully', 200
