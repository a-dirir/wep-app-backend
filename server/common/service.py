
class BaseService:
    def __init__(self):
        self.name = 'BaseService'
        self.controllers = {}

    def handle(self, payload: dict, controller: str, method: str):
        if self.controllers.get(controller) is None:
            return {'error': f"The controller {controller} is invalid for the service {self.name}"}, 400

        try:
            msg, status_code = self.controllers[controller].handle(payload, method)
            return msg, status_code
        except Exception as e:
            print(e)
            return {'error': e}, 400

