from server.common.crud import SimpleCRUD
from server.common.service import BaseService
from server.services.customers.controllers.client import Client
from server.services.customers.controllers.opportunity import Opportunity
from server.services.customers.controllers.sub_client import SubClient


class Customers(BaseService):
    def __init__(self):
        super().__init__()
        self.name = 'Customers'
        self.controllers = {
            'Client': Client('clients'),
            'SubClient': SubClient('sub_clients'),
            'Contact': SimpleCRUD('clients_contacts'),
            'Synthetic': SimpleCRUD('clients_url'),
            'AwsAccount': SimpleCRUD('aws_accounts'),
            'AzureAccount': SimpleCRUD('azure_accounts'),
            'M365Account': SimpleCRUD('m365_accounts'),
            'Opportunity': Opportunity('opportunities'),
            'AwsOpportunity': SimpleCRUD('aws_opportunity_details'),
            'AzureOpportunity': SimpleCRUD('azure_opportunity_details'),
            'M365Opportunity': SimpleCRUD('m365_opportunity_details'),
            'Addon': SimpleCRUD('addons'),
            'Product': SimpleCRUD('products'),
        }

