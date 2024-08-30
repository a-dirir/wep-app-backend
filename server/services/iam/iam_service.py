from server.base.service import BaseService
from server.services.iam.controllers.user_controller import User


class IAMService(BaseService):
    def __init__(self):
        super().__init__()
        self.name = 'IAM'

        self.controllers = {
            'User': User(),
        }

        self.allowed_controllers = ['User']
