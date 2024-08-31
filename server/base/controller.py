# Base class for controllers to inherit from to provide a common interface for handling requests
# The handle method is used to route the request to the appropriate method
# The method is determined by the method parameter
class BaseController:
    def __init__(self):
        self.name = 'BaseController'
        self.methods = []

    def handle(self, payload: dict, method: str):
        if method not in self.methods:
            return {'error': f"The method {method} is invalid for the controller {self.name}"}, 400

        msg, status_code = getattr(self, method)(payload)

        return msg, status_code
