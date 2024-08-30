from server.base.service import BaseService
from server.services.common.controllers.records_linker import RecordsLinker


class CommonService(BaseService):
    def __init__(self):
        super().__init__()
        self.name = 'Common'
        self.controllers = {
            'RecordsLinker': RecordsLinker()
        }
        self.allowed_controllers = ['RecordsLinker']
