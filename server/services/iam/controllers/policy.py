from server.services.iam.models.iam_models import PolicyModel
from sqlalchemy.orm import Session


class Policy:
    def __init__(self):
        pass

    def createPolicy(self, payload: dict):
        data = payload['data']
        db = payload['db']

        # add validation

        data['expanded_policy'] = Policy._expandPolicy(data['policy'])

        with Session(db.engine) as session:
            try:
                policy = PolicyModel(
                    name=data['name'],
                    description=data['description'],
                    policy=data['policy'],
                    expanded_policy=data['expanded_policy']
                )

                session.add(policy)
                session.commit()
            except Exception as e:
                print(e)
                return {'error': 'Failed to create Policy'}, 400


        return {}, 200

    def getPolicy(self, payload: dict):
        data = payload['data']
        db = payload['db']

        # add validation

        with Session(db.engine) as session:
            try:
                policy = session.query(PolicyModel).filter_by(name=data['name']).first().to_dict()
            except Exception as e:
                print(e)
                return {'error': 'Failed to get Policy'}, 400

        return policy, 200

    def getPolicies(self, payload: dict):
        db = payload['db']

        with Session(db.engine) as session:
            try:
                policies = session.query(PolicyModel).all()
                policies = [policy.to_dict() for policy in policies]
            except Exception as e:
                print(e)
                return {'error': 'Failed to get Policies'}, 400

        return policies, 200

    def updatePolicy(self, payload: dict):
        data = payload['data']
        db = payload['db']

        # add validation

        data['expanded_policy'] = self._expandPolicy(data['policy'])

        with Session(db.engine) as session:
            try:
                policy = session.query(PolicyModel).filter_by(name=data['name']).first()
                policy.description = data['description']
                policy.policy = data['policy']
                policy.expanded_policy = data['expanded_policy']

                session.commit()
            except Exception as e:
                print(e)
                return {'error': 'Failed to update Policy'}, 400

        return {}, 200

    def deletePolicy(self, payload: dict):
        data = payload['data']
        db = payload['db']

        # add validation

        with Session(db.engine) as session:
            try:
                policy = session.query(PolicyModel).filter_by(name=data['name']).first()
                session.delete(policy)
                session.commit()
            except Exception as e:
                print(e)
                return {'error': 'Failed to delete Policy'}, 400

        return {}, 200

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






