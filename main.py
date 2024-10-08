import os
import datetime

from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from dotenv import load_dotenv

from server.api.router import Router
from server.api.authenticator import Authenticator
from server.database.mysql_db import MySQLDB
from server.util import get_logger


# Below User class is required for flask_login
class User(UserMixin):
    def __init__(self, _id):
        self.id = _id
        self.username = _id


# Load environment variables
def load_env(env: str = 'local'):
    if env == 'local':
        load_dotenv("config.env")


def setup():
    # Load environment variables
    load_env()

    # Create Flask app, LoginManager
    app_local = Flask(__name__)
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

    # create instance of MySQLDB, Router, Authenticator and Logger
    db_local = MySQLDB()
    router_local = Router()
    authenticator_local = Authenticator(db_local)
    logger_local = get_logger(__name__)

    return app_local, login_manager_local, db_local, router_local, authenticator_local, logger_local


app, login_manager, db, router, authenticator, logger = setup()


# Required for flask_login
@login_manager.user_loader
def user_loader(username):
    return User(username)


# handle login request
@app.route('/login', methods=['POST'])
def login():
    # get username and password from request headers
    username = request.headers.get('username')
    password = request.headers.get('password')

    if username is None or password is None:
        return jsonify(msg={'error': 'Missing username or password'}), 400

    payload = {'username': username, 'password': password}
    if not authenticator.is_authentic(payload):
        return jsonify(msg={'error': 'Invalid username or password'}), 400

    # login user in flask_login
    login_user(User(username), remember=True, duration=datetime.timedelta(seconds=24 * 60 * 60))

    # return user info to client containing username and group
    user_info = {'username': username, 'group': authenticator.get_user_group(username)}

    response = make_response(
        jsonify(msg={'user_info': user_info})
    )

    return response


# handle status request that checks if user is logged in
@login_required
@app.route('/status', methods=['POST'])
def status():
    if current_user.is_authenticated:
        user_info = {'username': current_user.username,
                     'group': authenticator.get_user_group(current_user.username)}

        return jsonify(msg={'user_info': user_info}), 200
    else:
        return jsonify(msg="Not logged in"), 401


# handle logout request
@app.route("/logout", methods=["POST"])
@login_required
def logout():
    if current_user.is_authenticated:
        # logout user in flask_login
        logout_user()
        response = make_response(jsonify(msg="Logged out successfully"), 200)
        return response
    else:
        return jsonify(msg="User is not logged in"), 401


# handle application request that routes the request to the appropriate service, controller and method
# and returns the response to the client
@app.route('/app', methods=['POST'])
@login_required
def application():
    try:
        if not current_user.is_authenticated:
            return jsonify(msg='User is not authenticated'), 401

        # load json data from request, add db, router and user info to payload
        payload = request.get_json()
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
            return jsonify(msg), status_code

    except Exception as e:
        logger.error(f"Error: {e}")
        msg = {'error': 'The server encountered an internal error and was unable to complete your request'}
        status_code = 500

    return jsonify(msg=msg), status_code


if __name__ == '__main__':
    app.run(debug=True, port=80)
