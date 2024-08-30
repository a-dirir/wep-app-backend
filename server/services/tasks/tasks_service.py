from server.base.crud_new import CRUDNew
from server.base.service import BaseService


class TasksService(BaseService):
    def __init__(self):
        super().__init__()
        self.name = 'Tasks'
        self.controllers = {
            '*': CRUDNew(self.name)
        }
        self.allowed_controllers = ['Tasks', 'TaskHistory']
