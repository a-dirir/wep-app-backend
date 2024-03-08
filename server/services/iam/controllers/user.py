import hashlib
from datetime import datetime
import os


class User:
    def __init__(self):
        self.table_name = 'iam_users'

    @staticmethod
    def generateCredentials():
        # generate the salt
        salt = os.urandom(32).hex()
        # generate a random string of length 64bytes for the key value
        password = os.urandom(2).hex()
        # hash the key value with the salt
        password_hashed = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000).hex()

        return salt, password, password_hashed

    def create(self, payload: dict):
        data = payload['data']
        db = payload['db']
        user = payload['user']

        if user['type'] != 'user':
            return {'error': 'Only users can create api keys'}, 400

        salt, password, password_hashed = self.generateCredentials()

        # add validation
        if data.get('email') is None or data.get('name') is None or data.get('user_group') is None:
            return {'error': 'Missing required fields'}, 400

        # insert row into table
        row = {
            'email': data['email'],
            'name': data['name'],
            'user_group': data['user_group'],
            'salt': salt,
            'password_hashed': password_hashed,
            'last_time_active': datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        }

        success, results = db.insert_row(table_name=self.table_name, row=row)

        if not success:
            return {'error': results}, 400

        credentials = {
            'email': data['email'],
            'password': password
        }

        return credentials, 200

    def read(self, payload: dict):
        data = payload['data']
        db = payload['db']

        # add validation
        if data.get('email') is None:
            return {'error': 'Missing required fields'}, 400

        # get row from table
        conditions = {'email': data['email']}
        success, results = db.get_row(table_name=self.table_name, where_items=conditions)

        if not success:
            return {'error': results}, 400

        return results, 200

    def list(self, payload: dict):
        db = payload['db']

        # get all rows from table
        success, results = db.get_rows(table_name=self.table_name)

        if not success:
            return {'error': results}, 400

        # remove the password_hashed and salt from the results
        for user in results:
            user.pop('password_hashed')
            user.pop('salt')

        return results, 200

    def delete(self, payload: dict):
        data = payload['data']
        db = payload['db']

        # add validation
        if data.get('email') is None:
            return {'error': 'Missing required fields'}, 400

        # delete row from table
        conditions = {'email': data['email']}
        success, results = db.delete_row(table_name=self.table_name, where_items=conditions)

        if not success:
            return {'error': results}, 400

        return results, 200

    def validate(self, payload: dict):
        data = payload['data']
        db = payload['db']

        # add validation
        if data.get('email') is None or data.get('password') is None:
            return {'error': 'Missing required fields'}, 400

        # get row from table
        conditions = {'email': data['email']}
        success, results = db.get_row(table_name=self.table_name, where_items=conditions)

        if not success:
            return {'error': results}, 400

        # hash the password with the salt and compare it to the stored password
        salt = results['salt']
        password_hashed = hashlib.pbkdf2_hmac('sha256', data.get('password').encode('utf-8'), salt.encode('utf-8'), 100000).hex()
        if password_hashed != results['password_hashed']:
            return {'error': 'Invalid credentials'}, 400

        # update the last_time_active field
        success, results = db.update_row(table_name=self.table_name,
                                         row={'last_time_active': datetime.now().strftime("%m/%d/%Y %H:%M:%S")}, where_items=conditions)

        if not success:
            return {'error': results}, 400

        return True, 200


