import hashlib
from server.util import get_logger


# class to authenticate users using username and password, and return their group.
class Authenticator:
    def __init__(self, db):
        self.table_name = 'iam_users'
        self.db = db
        self.cache = {}
        self.logger = get_logger(self.__class__.__name__)

    def is_authentic(self, user_credential: dict):
        username = user_credential.get('username')
        password = user_credential.get('password')

        conditions = {'email': username}

        success, results = self.db.get(table_name=self.table_name, where_items=[conditions])
        if not success or len(results) == 0:
            return False

        true_password_hashed = results[0].get('password_hashed')
        salt = results[0].get('salt')

        self.cache[username] = {'group': results[0].get('user_group')}

        if not self.verify_password(password, true_password_hashed, salt):
            return False

        return True

    @staticmethod
    def verify_password(password: str, true_password_hash: str, salt: str):
        # hash the password with the salt and compare it to the stored password
        given_password_hashed = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'),
                                                    salt.encode('utf-8'), 100000).hex()
        if given_password_hashed != true_password_hash:
            return False

        return True

    def get_user_group(self, username: str):
        if username in self.cache:
            return self.cache[username].get('group')

        return None
