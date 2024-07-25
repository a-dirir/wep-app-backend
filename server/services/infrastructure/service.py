from server.common.crud import CRUD
from server.common.service import BaseService
from server.common.mappings import controller_db_mappings
from server.services.infrastructure.controllers.alarm.triggered import TriggeredAlarms


class Infrastructure(BaseService):
    def __init__(self):
        super().__init__()
        self.name = 'Infrastructure'
        self.controllers = {
            'TriggeredAlarms': TriggeredAlarms()
        }
        self.allowed_controllers = list(controller_db_mappings.keys())
        self.allowed_controllers.extend([key for key in self.controllers.keys() if key != '*'])
