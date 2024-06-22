import os
import datetime
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask import render_template, send_from_directory


from server.api.router import Router
from server.api.authenticator import Authenticator
from server.database.mysql_db import MySQLDB
from server.util import get_logger


login_manager = LoginManager()


class User(UserMixin):
    def __init__(self, _id):
        self.id = _id
        self.username = _id


class Server:
    def __init__(self, db: MySQLDB, website_dir: str):
        self.db = db
        self.website_dir = website_dir
        self.app = Flask(__name__, static_folder=self.website_dir, template_folder="../../static_files")
        self.app.config["SECRET_KEY"] = os.urandom(24)
        self.app.config['SESSION_COOKIE_SAMESITE'] = 'None'
        self.app.config['REMEMBER_COOKIE_SAMESITE'] = 'None'
        self.app.config['SESSION_COOKIE_SECURE'] = True
        self.app.config['REMEMBER_COOKIE_SECURE'] = True
        login_manager.init_app(self.app)
        login_manager.session_protection = "strong"

        cors = CORS(self.app, supports_credentials=True, resources={r"/*": {"origins": "*"}})

        self.router = Router()
        self.authenticator = Authenticator(self.db)
        self.logger = get_logger(__name__)

        self.routes()
        # self.app.run(host="0.0.0.0", port=8080, debug=True)

    @staticmethod
    @login_manager.user_loader
    def user_loader(username):
        return User(username)

    def routes(self):
        @self.app.route('/login', methods=['POST'])
        def login():
            if current_user.is_authenticated:
                return jsonify(msg="Already logged in"), 200

            username = request.headers.get('username')
            password = request.headers.get('password')

            if username is None or password is None:
                return jsonify(msg={'error': 'Missing username or password'}), 400

            payload: dict = {'username': username, 'password': password}
            if not self.authenticator.is_authentic(payload):
                return jsonify(msg={'error': 'Invalid username or password'}), 400

            login_user(User(username), remember=True, duration=datetime.timedelta(seconds=24*60*60))

            user_info = {'username': username, 'group': self.authenticator.get_user_group(username)}

            response = make_response(jsonify(msg=user_info))

            return response

        @self.app.route('/status', methods=['POST'])
        def status():
            if current_user.is_authenticated:
                user_info = {'username': current_user.username,
                             'group': self.authenticator.get_user_group(current_user.username)}
                return jsonify(msg=user_info), 200
            else:
                return jsonify(msg="Not logged in"), 400

        @self.app.route("/logout", methods=["POST"])
        @login_required
        def logout():
            if current_user.is_authenticated:
                logout_user()
                return jsonify(msg="Logged out successfully"), 200
            else:
                return jsonify(msg="User is not logged in"), 400

        @self.app.route('/app', methods=['POST'])
        @login_required
        def app1():
            if not current_user.is_authenticated:
                return jsonify(msg='User is not authenticated'), 400

            # load json data from request
            payload: dict = request.get_json()
            payload['db'] = self.db
            payload['router'] = self.router

            user_group = self.authenticator.get_user_group(current_user.username)
            if user_group is None:
                return jsonify(msg={'error': 'User is not authenticated'}), 400

            payload['user'] = {'username': current_user.username, 'group': user_group}

            # route the request to the appropriate service, controller and method
            msg, status_code = self.router.route(payload)

            # return a flask response object to the client
            if status_code == 200:
                return jsonify(msg=msg), status_code
            else:
                return jsonify(msg['error']), status_code

        @self.app.route('/', methods=['GET'])
        def index():
            print(os.getcwd())
            return send_from_directory(self.website_dir, 'index.html')

        @self.app.route('/<path:path>')
        def serve_static(path):
            # Check if the file exists in the static folder
            file_path = os.path.join(self.website_dir, path)
            if os.path.isfile(file_path):
                return send_from_directory(self.website_dir, path)
            else:
                # Return a 404 error if the file does not exist
                return make_response(jsonify({'error': 'File not found'}), 404)

