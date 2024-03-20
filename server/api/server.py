import os
from flask import Flask, request, jsonify
from flask_cors import CORS

from server.api.router import Router
from server.api.authenticator import Authenticator
from server.database.mysql_db import MySQLDB
from server.util import get_logger


class Server:
    def __init__(self, db: MySQLDB):
        self.db = db
        self.app = Flask(__name__)
        cors = CORS(self.app)
        self.router = Router()
        self.authenticator = Authenticator(self.db)
        self.logger = get_logger(__name__)

        self.routes()
        self.app.run(host="0.0.0.0", port=os.getenv("API_Server_Port"))

    def routes(self):
        @self.app.route('/', methods=['POST'])
        def app():
            # get user credentials from request header
            user_id = request.headers.get('user-id')
            user_password = request.headers.get('user-password')
            user_type = request.headers.get('user-type')

            # check if user credentials are available
            if user_id is None or user_password is None or user_type is None:
                self.logger.error(f"User failed to provide required credentials")
                return jsonify(msg='User credentials are missing'), 400

            user = {'id': user_id, 'type': user_type, 'secret': user_password}
            # check if user credentials are valid
            if not self.authenticator.authenticate(user):
                self.logger.error(f"User {user['id']} failed to authenticate")
                return jsonify(msg='Authentication failed'), 400

            # load json data from request
            request_msg: dict = request.get_json()

            # check if request action is available
            if request_msg.get('access') is None or request_msg.get('data') is None:
                self.logger.error(f"User {user['id']} failed to provide required access or data")
                return jsonify(msg='Requested access or required data is missing'), 400

            payload = {
                'data': request_msg['data'],
                'access': request_msg['access'],
                'user': user, 'router': self.router,
                'db': self.db
            }

            # route the request to the appropriate service, controller and method
            msg, status_code = self.router.route(payload)

            # return a flask response object to the client
            if status_code == 200:
                return jsonify(msg=msg), status_code
            else:
                return jsonify(msg['error']), status_code




