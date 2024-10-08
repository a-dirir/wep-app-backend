from server.api.policies import policies

"""
Class to authorize users based on their group and the access they are trying to perform.
The policies are defined in the policies.py file. A policy is a dictionary with the following structure:
{
    'version': '1.0',
    'statements': [
        {
            'effect': 'allow',
            'actions': ['service:controller:method'],
            'resources': ['some resource']
        },
        {
            'effect': 'deny',
            'actions': ['service:controller:method'],
            'resources': ['some resource']
        }
    ]
}
A deny statement will always take precedence over an allow statement. 
If an action is not defined in an allow policy, the user will not be authorized to perform that action.
"""


class Authorizer:
    def __init__(self):
        self.policies = {}
        self.cache = {}

        for group, policy in policies.items():
            self.policies[group] = self._expandPolicy(policy)
            self.cache[group] = {}

    def is_authorized(self, group: str, access: dict):
        if self.cache.get(group) is None:
            return False

        # flush cache if cache is larger than 100
        if len(self.cache[group]) > 100:
            self.cache[group] = {}

        _id = f"{access['action']}:{access['resource']}"
        if self.cache[group].get(_id) is None:
            self.cache[group][_id] = self.check_policy(group, access)

        return self.cache[group][_id]

    def check_policy(self, group: str, access: dict):
        action = access.get('action')
        resource = access.get('resource')

        if action is None or resource is None:
            return False

        if self.policies.get(group) is None:
            return False

        # check for * wildcard
        if '*' in self.policies[group]['permissions']:
            if self.check_action(group, '*', resource):
                return True

        # check for specific action
        if self.policies[group]['permissions'].get(action) is not None:
            if self.check_action(group, action, resource):
                return True

        return False

    def check_action(self, group: str, action: str, resource: str):
        permission = self.policies[group]['permissions'].get(action)
        if permission is None:
            return False

        # check for deny effect
        if permission.get('deny') is not None:
            # check for * wildcard
            if resource in permission['deny']['resources'] or '*' in permission['deny']['resources']:
                return False

        # check for allow effect
        if permission.get('allow') is not None:
            # check for * wildcard
            if resource in permission['allow']['resources'] or '*' in permission['allow']['resources']:
                return True

        return False

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
                            'resources': statement['resources']
                        }
                    }

                elif permissions[action].get(statement['effect']) is None:
                    permissions[action][statement['effect']] = {
                        'resources': statement['resources']
                    }

                else:
                    current_resources = permissions[action][statement['effect']]['resources']
                    # add new resources to the current resources
                    for resource in statement['resources']:
                        if resource not in current_resources:
                            current_resources.append(resource)

                    permissions[action][statement['effect']] = {
                        'resources': current_resources
                    }

        expanded_policy = {
            "version": policy['version'],
            "permissions": permissions
        }

        return expanded_policy
