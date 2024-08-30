from server.base.crud_new import CRUDNew
from server.base.service import BaseService


class DepartmentsService(BaseService):
    def __init__(self):
        super().__init__()
        self.name = 'Departments'
        self.controllers = {
            '*': CRUDNew(self.name)
        }
        self.allowed_controllers = ['Departments', 'DepartmentManagers', 'DepartmentEmployees']
