from server.base.crud import CRUD
from server.base.service import BaseService
from server.services.employees.controllers.leave_history_controller import LeaveHistory


# EmployeesService class is a child class of BaseService class
# It is used to define the Employees service and its controllers
# only one custom controllers is defined in the Employees service, all controllers use the CRUD class
# The LeaveHistory controller is used to manage the leave history of employees
class EmployeesService(BaseService):
    def __init__(self):
        super().__init__()
        self.name = 'Employees'
        self.controllers = {
            'LeaveHistory': LeaveHistory(),
            '*': CRUD(self.name),
        }

        self.allowed_controllers = ['Employees', 'Titles', 'Salaries', 'LeaveBalances', 'LeaveHistory']