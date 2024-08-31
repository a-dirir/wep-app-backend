from server.base.service import BaseService
from server.services.common.controllers.records_linker import RecordsLinker


# CommonService class is a child class of BaseService class
# It is used to define the controllers common in general
# The RecordsLinker controller is used to list all the records linked to a record in db
class CommonService(BaseService):
    def __init__(self):
        super().__init__()
        self.name = 'Common'
        self.controllers = {
            'RecordsLinker': RecordsLinker()
        }
        self.allowed_controllers = ['RecordsLinker']
