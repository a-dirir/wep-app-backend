from server.services.customers.controllers.simple_crud import SimpleCRUD
from server.services.customers.controllers.client import Client
from server.services.customers.controllers.contact import Contact


class Customers:
    def __init__(self):
        self.name = 'Customers'

        self.handlers = {
            'Client': Client('clients'),
            'SubClient': Client('sub_clients'),
            'Contact': Contact('clients_contacts'),
            'Synthetic': SimpleCRUD('clients_url'),

            'AwsAccount': SimpleCRUD('aws_accounts'),
            'AzureAccount': SimpleCRUD('azure_accounts'),
            'M365Account': SimpleCRUD('m365_accounts'),

            'Opportunity': SimpleCRUD('opportunities'),
            'AwsOpportunity': SimpleCRUD('aws_opportunity_details'),
            'AzureOpportunity': SimpleCRUD('azure_opportunity_details'),
            'M365Opportunity': SimpleCRUD('m365_opportunity_details'),

            'Addon': SimpleCRUD('addons'),
            'Product': SimpleCRUD('products'),
        }

    def handle(self, payload: dict, handler: str, method: str):
        if self.handlers.get(handler) is None:
            return {'error': 'API Handler is invalid'}, 400

        try:
            handler_method = getattr(self.handlers[handler], method)
            msg, status_code = handler_method(payload)
            return msg, status_code
        except AttributeError as e:
            print(e)
            return {'error': 'API method is invalid'}, 400
        except Exception as e:
            print(e)
            return {'error': 'Some error happened, please try again'}, 400




