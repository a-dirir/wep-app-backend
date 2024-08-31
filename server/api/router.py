from server.api.authorizer import Authorizer
from server.services.common.common_service import CommonService
from server.services.departments.departments_service import DepartmentsService
from server.services.employees.employees_service import EmployeesService
from server.services.iam.iam_service import IAMService
from server.services.tasks.tasks_service import TasksService
from server.util import get_logger


# A router class that routes the request to the appropriate service, controller and method
# based on the action provided in the request. It also checks if the user is authorized to
# perform the requested action. If the user is not authorized, it returns an error message.
# The router logs the request and response for each request.
class Router:
    def __init__(self):
        self.services = {
            'IAM': IAMService(),
            'Employees': EmployeesService(),
            'Departments': DepartmentsService(),
            'Tasks': TasksService(),
            'Common': CommonService()
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
