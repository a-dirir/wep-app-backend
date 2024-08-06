import json
import os
import datetime

import boto3
from flask import Flask, request, jsonify, make_response, send_from_directory, session
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from dotenv import load_dotenv

from server.api.router import Router
from server.api.authenticator import Authenticator
from server.database.mysql_db import MySQLDB
from server.util import get_logger


class User(UserMixin):
    def __init__(self, _id):
        self.id = _id
        self.username = _id


def load_env():
    load_dotenv("config.env")


def load_aws_env():
    try:
        secret_name = "crm-backend"
        region_name = "me-central-1"

        boto3_session = boto3.session.Session()
        client = boto3_session.client(
            service_name='secretsmanager',
            region_name=region_name
        )

        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )

        secret = json.loads(get_secret_value_response["SecretString"])

        for key, value in secret.items():
            os.environ[key] = str(value)

        return True
    except Exception as e:
        return False


def setup():
    success = load_aws_env()
    if not success:
        load_env()

    app_local = Flask(__name__, static_folder="static_files", template_folder="static_files")
    login_manager_local = LoginManager()
    app_local.config.update(
        SECRET_KEY=os.urandom(24),
        SESSION_COOKIE_SAMESITE='None',
        REMEMBER_COOKIE_SAMESITE='None',
        SESSION_COOKIE_SECURE=True,
        REMEMBER_COOKIE_SECURE=True
    )

    login_manager_local.init_app(app_local)
    login_manager_local.session_protection = "strong"

    cors = CORS(app_local, supports_credentials=True, resources={r"/*": {"origins": "*"}})

    return app_local, login_manager_local


app, login_manager = setup()


@login_manager.user_loader
def user_loader(username):
    return User(username)


@app.route('/login', methods=['POST'])
def login():
    username = request.headers.get('username')
    password = request.headers.get('password')

    if username is None or password is None:
        return jsonify(msg={'error': 'Missing username or password'}), 400

    payload: dict = {'username': username, 'password': password}
    if not authenticator.is_authentic(payload):
        return jsonify(msg={'error': 'Invalid username or password'}), 400

    login_user(User(username), remember=True, duration=datetime.timedelta(seconds=24 * 60 * 60))

    user_info = {'username': username,
                 'group': authenticator.get_user_group(username)
                 }

    response = make_response(
        jsonify(msg={'user_info': user_info, 'customers': authenticator.get_customers()})
    )

    return response


@login_required
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
        logger.info(f"Success: {msg}")
        return jsonify(msg=msg), status_code
    else:
        logger.error(f"Error: {msg}")
        return jsonify(msg['error']), status_code


if __name__ == '__main__':
    db = MySQLDB()
    router = Router()
    authenticator = Authenticator(db)
    logger = get_logger(__name__)
    app.run(debug=True, port=80)


