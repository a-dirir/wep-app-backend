import logging

from server.authorizer import Authorizer
from server.services.customers.service import Customers
from server.services.iam.service import IAM


class Router:
    def __init__(self):
        self.services = {
            'IAM': IAM(),
            'Customers': Customers(),
        }
        self.authorizer = Authorizer()

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(fmt="%(asctime)s %(levelname)s %(message)s",
                                      datefmt="%Y-%m-%d %H:%M:%S")
        fh = logging.FileHandler("server.log", "a")
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

    def route(self, payload: dict):
        access = payload['access']
        user = payload['user']['id']

        # check if user is authorized to access the requested resource
        if not self.authorizer.is_authorized(payload):
            return {'error': f"User is not authorized to perform the action {access}"}, 400

        # extract service, controller and method from request action
        action = access['action'].split(':')
        service = str(action[0]); controller = str(action[1]); method = str(action[2])

        if self.services.get(service) is None:
            return {'error': 'API Service is invalid'}, 400

        msg, status_code = self.services[service].handle(payload, controller, method)

        # log request
        self.logger.info(f"{user['id']} {access['action']} {access['customers']} {access['resources']} {status_code}")

        return msg, status_code

