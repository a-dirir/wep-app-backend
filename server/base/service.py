# Base class for services to inherit from to provide a common interface for handling requests
# The handle method is used to route the request to the appropriate controller
# The controller is determined by the controller key in the payload
# The method is determined by the method key in the payload
class BaseService:
    def __init__(self):
        self.name = 'BaseService'
        self.controllers = {}
        self.allowed_controllers = []

    def handle(self, payload: dict, controller: str, method: str):
        if controller not in self.allowed_controllers:
            return {'error': f"The controller {controller} is invalid for the service {self.name}"}, 400

        try:
            payload['service'] = self.name
            payload['controller'] = controller

            if controller in self.controllers:
                msg, status_code = self.controllers[controller].handle(payload, method)
            else:
                msg, status_code = self.controllers['*'].handle(payload, method)

            return msg, status_code
        except Exception as e:
            return {'error': e}, 400

