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
        self.app.run(host="0.0.0.0", port=8081, debug=True)

    def routes(self):
        @self.app.route('/auth', methods=['POST'])
        def auth():
            return jsonify(msg='salam'), 200

        @self.app.route('/app', methods=['POST'])
        def app():
            # load json data from request
            payload: dict = request.get_json()
            payload['db'] = self.db
            payload['router'] = self.router

            # route the request to the appropriate service, controller and method
            msg, status_code = self.router.route(payload)

            # return a flask response object to the client
            if status_code == 200:
                return jsonify(msg=msg), status_code
            else:
                return jsonify(msg['error']), status_code
