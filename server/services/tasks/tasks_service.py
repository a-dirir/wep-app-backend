from server.base.crud import CRUD
from server.base.service import BaseService


# TasksService class is a child class of BaseService class
# It is used to define the Tasks service and its controllers
# No custom controllers are defined for the Tasks service, all controllers use the CRUD class
class TasksService(BaseService):
    def __init__(self):
        super().__init__()
        self.name = 'Tasks'
        self.controllers = {
            '*': CRUD(self.name)
        }
        self.allowed_controllers = ['Tasks', 'TaskHistory']
