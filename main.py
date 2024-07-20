import os
import datetime
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask import send_from_directory
from dotenv import load_dotenv


from server.api.router import Router
from server.api.authenticator import Authenticator
from server.database.mysql_db import MySQLDB
from server.util import get_logger


class User(UserMixin):
    def __init__(self, _id):
        self.id = _id
        self.username = _id


def load_db():
    return MySQLDB()


load_dotenv("config.env")
app = Flask(__name__, static_folder="static_files", template_folder="static_files")
login_manager = LoginManager()
app.config["SECRET_KEY"] = os.urandom(24)
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['REMEMBER_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = True
app.config['REMEMBER_COOKIE_SECURE'] = True
login_manager.init_app(app)
login_manager.session_protection = "strong"

cors = CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})

db = load_db()
router = Router()
authenticator = Authenticator(db)
logger = get_logger(__name__)


@login_manager.user_loader
def user_loader(username):
    return User(username)


@app.route('/login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        user_info = {'username': current_user.username,
                     'group': authenticator.get_user_group(current_user.username),
                     'customers': authenticator.get_customers(),
                     }

        return jsonify(msg={'user_info': user_info, 'customers': authenticator.get_customers()}), 200

    username = request.headers.get('username')
    password = request.headers.get('password')

    if username is None or password is None:
        return jsonify(msg={'error': 'Missing username or password'}), 400

    payload: dict = {'username': username, 'password': password}
    if not authenticator.is_authentic(payload):
        return jsonify(msg={'error': 'Invalid username or password'}), 400

    login_user(User(username), remember=True, duration=datetime.timedelta(seconds=24 * 60 * 60))

    user_info = {'username': username,
                 'group': authenticator.get_user_group(username),
                 'customers': authenticator.get_customers(),
                 }

    response = make_response(
        jsonify(msg={'user_info': user_info, 'customers': authenticator.get_customers()})
    )

    return response


@app.route('/status', methods=['POST'])
def status():
    if current_user.is_authenticated:
        user_info = {'username': current_user.username,
                     'group': authenticator.get_user_group(current_user.username),
                     }

        return jsonify(msg={'user_info': user_info, 'customers': authenticator.get_customers()}), 200
    else:
        return jsonify(msg="Not logged in"), 401


@app.route("/logout", methods=["POST"])
@login_required
def logout():
    if current_user.is_authenticated:
        logout_user()
        response = make_response(jsonify(msg="Logged out successfully"), 200)
        return response
    else:
        return jsonify(msg="User is not logged in"), 401


@app.route('/app', methods=['POST'])
@login_required
def application():
    if not current_user.is_authenticated:
        return jsonify(msg='User is not authenticated'), 401

    # load json data from request
    payload: dict = request.get_json()
    payload['db'] = db
    payload['router'] = router

    user_group = authenticator.get_user_group(current_user.username)
    if user_group is None:
        return jsonify(msg={'error': 'User is not authenticated'}), 401

    payload['user'] = {'username': current_user.username, 'group': user_group}

    # route the request to the appropriate service, controller and method
    msg, status_code = router.route(payload)

    # return a flask response object to the client
    if status_code == 200:
        return jsonify(msg=msg), status_code
    else:
        print(msg)
        return jsonify(msg['error']), status_code


# @app.route('/', methods=['GET'])
# def index():
#     absolute_path = os.path.abspath('static_files')
#     return send_from_directory(absolute_path, 'index.html')
#
#
# @app.route('/<path:path>')
# def serve_static(path):
#     return send_from_directory('static_files', path)


if __name__ == '__main__':
    app.run(debug=True, port=80)