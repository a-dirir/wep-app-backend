from server.database.simple_crud import SimpleCRUD
from server.services.customers.controllers.client import Client


class Customers:
    def __init__(self):
        self.name = 'Customers'

        self.controllers = {
            'Client': Client('clients'),
            'SubClient': Client('sub_clients'),
            'Contact': SimpleCRUD('clients_contacts'),
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

    def handle(self, payload: dict, controller: str, method: str):
        if self.controllers.get(controller) is None:
            return {'error': 'API Controller is invalid'}, 400

        try:
            controller_method = getattr(self.controllers[controller], method)
            msg, status_code = controller_method(payload)
            return msg, status_code
        except AttributeError as e:
            print(e)
            return {'error': 'API method is invalid'}, 400
        except Exception as e:
            print(e)
            return {'error': 'Some error happened, please try again'}, 400




