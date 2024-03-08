from server.database.simple_crud import SimpleCRUD
from server.services.iam.controllers.policy import Policy
from server.services.iam.controllers.api_keys import ApiKey
from server.services.iam.controllers.user import User


class IAM:
    def __init__(self):
        self.name = 'IAM'

        self.controllers = {
            'User': User(),
            'Group': SimpleCRUD(table_name='iam_groups'),
            'Policy': Policy(),
            'ApiKey': ApiKey()
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




