
from server.services.iam.controllers.user import User
from server.services.iam.controllers.group import Group
from server.services.iam.controllers.policy import Policy
from server.services.iam.controllers.api_keys import ApiKey
from server.services.iam.controllers.customer import Customer


class IAM:
    def __init__(self):
        self.name = 'IAM'

        self.handlers = {
            'User': User(),
            'Group': Group(),
            'Policy': Policy(),
            'ApiKey': ApiKey(),
            'Customer': Customer()
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




