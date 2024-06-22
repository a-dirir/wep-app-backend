from server.util import get_logger


class BaseController:
    def __init__(self):
        self.name = 'BaseController'
        self.methods = []
        self.logger = get_logger(__name__)

    def handle(self, payload: dict, method: str):
        if method not in self.methods:
            return {'error': f"The method {method} is invalid for the controller {self.name}"}, 400

        msg, status_code = getattr(self, method)(payload)

        return msg, status_code
