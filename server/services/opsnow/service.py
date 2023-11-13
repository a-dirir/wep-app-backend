from server.services.opsnow.controllers.customers import Customers
from server.services.opsnow.controllers.asset import Asset

access_token = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICIzYjVKbFExeUI1Z0lWeXpkbFFMeXAxLVFOeHVLbEFIYnZzbUh4dTU5eThvIn0.eyJleHAiOjE2OTgyNDg5OTksImlhdCI6MTY5ODI0NTM5OSwiYXV0aF90aW1lIjoxNjk4MjQ1Mzk3LCJqdGkiOiJkMzFhNDk1OS0yYjhkLTQ1YWEtYTIwNy1iMjYwOTdmZTdjOGIiLCJpc3MiOiJodHRwczovL3Nzby5vcHNub3cubWUvYXV0aC9yZWFsbXMvQkdNRUEiLCJhdWQiOlsiZmlub3BzX2JhY2siLCJhY2NvdW50Il0sInN1YiI6IjJmOTQwN2NlLWYyNGQtNDQzYy05M2E2LWVhZTAxNmM3Y2M0NCIsInR5cCI6IkJlYXJlciIsImF6cCI6ImZpbm9wc19mcm9udCIsIm5vbmNlIjoiMmVmYTlmNTgtNTNkMi00MzMzLThkYzQtOWNiMzdlYzlhOWE5Iiwic2Vzc2lvbl9zdGF0ZSI6ImMyNjEzYTY4LTYwOTEtNGE4MC1hZjJlLTM2MGQ0NDNiMGE0ZCIsImFjciI6IjAiLCJhbGxvd2VkLW9yaWdpbnMiOlsiKiJdLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsib2ZmbGluZV9hY2Nlc3MiLCJ1bWFfYXV0aG9yaXphdGlvbiJdfSwicmVzb3VyY2VfYWNjZXNzIjp7ImZpbm9wc19iYWNrIjp7InJvbGVzIjpbInVtYV9wcm90ZWN0aW9uIl19LCJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwiaXNzdWVyX3R5cGUiOiJjbXAiLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsInNpdGVDZCI6IkJHTUVBIiwicHJlZmVycmVkX3VzZXJuYW1lIjoiYWhtZWQuZGlyaXJAYmVzcGluZ2xvYmFsLmFlIiwidG9rZW5fdHlwZSI6ImxvZ2luIiwiZW1haWwiOiJhaG1lZC5kaXJpckBiZXNwaW5nbG9iYWwuYWUifQ.y8aNHHX6yy-8XIzvSHku2ZLOSmDjyd2Zkf0GiRWx82WZApNLFvj6nHWEKEf9GT1EXtKStrLrNz0K9y0j7YiGvWGJ8ozDhnLRH__nufrTD34U_ycEf8wRX2wzqMh8-awUqyTr6O_hZ_lmvRSTZWfySTye2aAYSE3DYACLdqIksRz6WCsY-nhksgiYojphBhi6rGD8VN8mdSbvWjD4mFMKz06tO2mW8rUFnoxO4WhxTA6bJ7SKRr_7N4IPfVA0cD_E-lBeoKkDqADTzYeWNYr5DFo7d3Wtb3D_alry9CZ4ErtKotB993a5oojOz4piZQVsSqW1yrAT1Ix2m6et4ylf8A"

class OPSNOW:
    def __init__(self):
        self.name = 'OPSNOW'

        self.handlers = {
            'Customers': Customers(),
            'Asset': Asset()
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




