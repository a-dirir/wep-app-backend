import logging
from sqlalchemy.orm import Session
from server.services.iam.service import IAM
from server.services.opsnow.service import OPSNOW
from server.services.monitoring.service import Monitoring
from server.services.iam.models.iam_models import *



class Router:
    def __init__(self):
        self.services = {
            'IAM': IAM(),
            'OPSNOW': OPSNOW(),
            'Monitoring': Monitoring()
        }
        self.users = {}
        self.groups = {}
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(fmt="%(asctime)s %(levelname)s %(message)s",
                                      datefmt="%Y-%m-%d %H:%M:%S")
        fh = logging.FileHandler("server.log", "a")
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

    def route(self, payload: dict):
        access = payload['access']
        user = payload['user']
        db = payload['db']

        if not self.check_authorization(user, access, db):
            return {'error': f"You are not authorized to perform the action"}, 400

        action = access['action'].split(':')

        # extract service, controller and method from request action
        service = str(action[0]); handler = str(action[1]); method = str(action[2])

        if self.services.get(service) is None:
            return {'error': 'API Service is invalid'}, 400

        msg, status_code = self.services[service].handle(payload, handler, method)

        # log request
        self.logger.info(f"{user['id']} {access['action']} {access['customers']} {access['resources']} {status_code}")

        return msg, status_code

    def check_authorization(self, user, access: dict, db):
        # check if the user is authorized to access the service
        action: str = access['action']
        customers: list = access.get('customers')
        resources: list = access.get('resources')


        # check if request action is valid
        if len(action) is None or customers is None or resources is None:
            return False

        if self.users.get(user['id']) is not None:
            policy = self.groups[self.users[user['id']]]
            return self.match_action_with_policy(action, customers, resources, policy)

        if user['type'] == 'user':
            # load user data from database
            with Session(db.engine) as session:
                try:
                    actor = session.query(UserModel).filter_by(email=user['id']).first().to_dict()
                    actor_group = session.query(GroupModel).filter_by(name=actor['group']).first().to_dict()
                except Exception as e:
                    print(e)
                    return False
        elif user['type'] == 'apikey':
            # load api key data from database
            with Session(db.engine) as session:
                try:
                    actor = session.query(APIKeyModel).filter_by(key_id=user['id']).first().to_dict()
                    actor_group = session.query(GroupModel).filter_by(name=actor['key_group']).first().to_dict()
                except Exception as e:
                    print(e)
                    return False
        else:
            return False


        # load group policies from database
        with Session(db.engine) as session:
            try:
                policy = session.query(PolicyModel).filter_by(name=actor_group['policy']).first().to_dict()['expanded_policy']

            except Exception as e:
                print(e)
                return False

        self.groups[actor_group['name']] = policy
        self.users[user['id']] = actor_group['name']

        return self.match_action_with_policy(action, customers, resources, policy)

    def match_action_with_policy(self, action, customers, resources, policy):
        permission = policy['permissions'].get('*')
        if permission is not None:
            check_ccess = self.check_resource_customer_access(permission, customers, resources)
            if not check_ccess:
                return False
            else:
                return True

        permission = policy['permissions'].get(action)

        if permission is None:
            return False

        check_ccess = self.check_resource_customer_access(permission, customers, resources)
        if not check_ccess:
            return False


        return True

    @staticmethod
    def check_resource_customer_access(permission, customers, resources):
        deny = permission.get('deny')
        allow = permission.get('allow')

        for customer in customers:
            if deny is not None:
                if customer in deny['customers']:
                    return False
            if allow is not None:
                if customer not in allow['customers'] and allow['customers'] != ['*']:
                    return False

        for resource in resources:
            if deny is not None:
                if resource in deny['resources']:
                    return False
            if allow is not None:
                if resource not in allow['resources'] and allow['resources'] != ['*']:
                    return False

        return True

