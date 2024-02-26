from server.services.customers.controllers.addon import Addon
from server.services.customers.controllers.aws_account import AwsAccount
from server.services.customers.controllers.azure_account import AzureAccount
from server.services.customers.controllers.client import Client
from server.services.customers.controllers.contacts import Contact
from server.services.customers.controllers.m365_account import M365Account
from server.services.customers.controllers.product import Product
from server.services.customers.controllers.sub_client import SubClient
from server.services.customers.controllers.synthetic import Synthetic


class Customers:
    def __init__(self):
        self.name = 'Customers'

        self.handlers = {
            'Client': Client(),
            'SubClient': SubClient(),
            'Synthetic': Synthetic(),
            'Contact': Contact(),
            'AwsAccount': AwsAccount(),
            'AzureAccount': AzureAccount(),
            'M365Account': M365Account(),
            'Product': Product(),
            'Addon': Addon(),
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




