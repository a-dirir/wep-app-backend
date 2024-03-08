import json
import logging
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

from server.router import Router
from server.authenticator import Authenticator
from server.database.mysql_db import MySQLDB


class Server:
    def __init__(self):
        self.db = MySQLDB(
            host=os.getenv("MYSQL_IP"),
            user=os.getenv("MYSQL_User"),
            password=os.getenv("MYSQL_Password"),
            database=os.getenv("MYSQL_Name")
        )

        self.app = Flask(__name__)
        cors = CORS(self.app)
        self.router = Router()
        self.authenticator = Authenticator(self.db)

        self.routes()
        self.app.run(host="0.0.0.0", port=os.getenv("API_Server_Port"))

    def routes(self):
        @self.app.route('/', methods=['POST'])
        def app():
            # get user credentials from request header
            user_id = request.headers.get('user-id')
            user_password = request.headers.get('user-password')
            user_type = request.headers.get('user-type')
            user = {'id': user_id, 'type': user_type, 'secret': user_password}
            # check if user credentials are valid
            if not self.authenticator.authenticate(user):
                return jsonify(msg='Authentication failed'), 400

            # load json data from request
            request_msg: dict = request.get_json()

            # check if request action is available
            if request_msg.get('access') is None or request_msg.get('data') is None:
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



if __name__ == '__main__':
    load_dotenv("config.env")
    server = Server()

