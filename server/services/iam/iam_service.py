from server.base.service import BaseService
from server.services.iam.controllers.user_controller import User


# IAMService class is a child class of BaseService class
# It is used to define the IAM service and its controllers
class IAMService(BaseService):
    def __init__(self):
        super().__init__()
        self.name = 'IAM'

        self.controllers = {
            'User': User(),
        }

        self.allowed_controllers = ['User']
