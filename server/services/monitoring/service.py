from server.services.monitoring.controllers.alarms_template import AlarmTemplate


class Monitoring:
    def __init__(self):
        self.name = 'Monitoring'

        self.handlers = {
            'AlarmTemplate': AlarmTemplate(),
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




