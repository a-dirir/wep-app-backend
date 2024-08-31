from server.base.crud import CRUD
from server.base.service import BaseService


# DepartmentsService class is a child class of BaseService class
# It is used to define the Departments service and its controllers
# No custom controllers are defined for the Departments service, all controllers use the CRUD class
class DepartmentsService(BaseService):
    def __init__(self):
        super().__init__()
        self.name = 'Departments'
        self.controllers = {
            '*': CRUD(self.name)
        }
        self.allowed_controllers = ['Departments', 'DepartmentManagers', 'DepartmentEmployees']
