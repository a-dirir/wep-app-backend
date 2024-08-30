from server.base.crud_new import CRUDNew
from server.base.service import BaseService
from server.services.employees.controllers.leave_history_controller import LeaveHistory


class EmployeesService(BaseService):
    def __init__(self):
        super().__init__()
        self.name = 'Employees'
        self.controllers = {
            'LeaveHistory': LeaveHistory(),
            '*': CRUDNew(self.name),
        }

        self.allowed_controllers = ['Employees', 'Titles', 'Salaries', 'LeaveBalances', 'LeaveHistory']