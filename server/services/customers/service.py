from server.common.crud import CRUD
from server.common.crud_new import CRUDNew
from server.common.service import BaseService
from server.services.customers.controllers.client import Client
from server.services.customers.controllers.opportunity import Opportunity
from server.services.customers.controllers.sub_client import SubClient
from server.common.mappings import controller_db_mappings


class Customers(BaseService):
    def __init__(self):
        super().__init__()
        self.name = 'Customers'
        self.controllers = {
            'Client': Client(),
            'SubClient': SubClient(),
            'Opportunity': Opportunity(),
            '*': CRUDNew(self.name)
        }
        self.allowed_controllers = list(controller_db_mappings[self.name].keys())
