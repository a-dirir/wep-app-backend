from server.api.authorizer import Authorizer
from server.services.customers.service import Customers
from server.services.iam.service import IAM
from server.services.infrastructure.service import Infrastructure
from server.util import get_logger


class Router:
    def __init__(self):
        self.services = {
            'IAM': IAM(),
            'Customers': Customers(),
            # 'Infrastructure': Infrastructure()
        }
        self.authorizer = Authorizer()

        self.logger = get_logger(__name__)

    def route(self, payload: dict):
        access = payload['access']
        user = payload['user']

        # check if user is authorized to access the requested resource
        if not self.authorizer.is_authorized(user['group'], access):
            self.logger.error(f"User {user['username']} is not authorized to perform the action {access}")
            return {'error': f"You are not authorized to perform the action {access}"}, 400

        # extract service, controller and method from request action
        action = access['action'].split(':')

        if len(action) != 3:
            self.logger.error(f"User {user['username']} failed to provide a valid action {access['action']}")
            return {'error': f'API action {access["action"]} is invalid'}, 400

        service = str(action[0]); controller = str(action[1]); method = str(action[2])

        if self.services.get(service) is None:
            self.logger.error(f"User {user['username']} failed to provide a valid service {service}")
            return {'error': f'API Service {service} is invalid'}, 400

        msg, status_code = self.services[service].handle(payload, controller, method)

        # log request
        if status_code == 200:
            self.logger.info(f"User {user['username']} performed action {access} successfully")

        else:
            self.logger.error(f"User {user['username']} failed to perform action {access} with error {msg}")

        return msg, status_code
