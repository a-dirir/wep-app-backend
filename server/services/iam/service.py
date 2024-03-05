from server.database.simple_crud import SimpleCRUD
from server.services.iam.controllers.group import Group
from server.services.iam.controllers.policy import Policy
from server.services.iam.controllers.api_keys import ApiKey


class IAM:
    def __init__(self):
        self.name = 'IAM'

        self.handlers = {
            'User': SimpleCRUD(table_name='iam_users'),
            'Group': SimpleCRUD(table_name='iam_groups'),
            'Policy': SimpleCRUD(table_name='iam_policies'),
            'ApiKey': ApiKey()
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




