import hashlib
import os
from server.common.crud import CRUD
from server.util import get_logger


class User(CRUD):
    def __init__(self):
        self.name = 'IAMUser'
        super().__init__(self.name)
        self.methods = ['create', 'list', 'update', 'delete', 'generateCredentials']
        self.logger = get_logger(__class__.__name__)

    def generateCredentials(self, payload: dict):
        table_name = 'iam_users'
        # generate the salt
        salt = os.urandom(32).hex()
        # generate a random string of length 64bytes for the key value
        password = os.urandom(16).hex()
        # hash the key value with the salt
        password_hashed = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000).hex()

        db = payload['db']

        email = payload['data'].get('email')

        if email is None:
            self.logger.error(f"User email is required to generate credentials")
            return {'error': 'User email is required to generate credentials'}, 400

        #  update the user with the new credentials
        success, results = db.update_row(table_name,
                                         {'salt': salt, 'password_hashed': password_hashed}, [{'email': email}])
        if not success:
            self.logger.error(f"Failed to update user {email} with new credentials")
            return {'error': results}, 400

        self.logger.info(f"Successfully generated credentials for user {email}")

        return {'data': {'email': email, 'password': password}}, 200
