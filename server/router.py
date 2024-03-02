import logging

from server.services.customers.service import Customers
from server.services.iam.service import IAM



class Router:
    def __init__(self):
        self.services = {
            'IAM': IAM(),
            'Customers': Customers(),
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

        action = access['action'].split(':')

        # extract service, controller and method from request action
        service = str(action[0]); handler = str(action[1]); method = str(action[2])

        if self.services.get(service) is None:
            return {'error': 'API Service is invalid'}, 400

        msg, status_code = self.services[service].handle(payload, handler, method)

        # log request
        self.logger.info(f"{user['id']} {access['action']} {access['customers']} {access['resources']} {status_code}")

        return msg, status_code

