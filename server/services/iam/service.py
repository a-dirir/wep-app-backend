from server.common.service import BaseService
from server.services.iam.controllers.user import User


class IAM(BaseService):
    def __init__(self):
        super().__init__()
        self.name = 'IAM'

        self.controllers = {
            'User': User(),
        }


print(User.__name__)