import hashlib
from datetime import datetime
import os


class ApiKey:
    def __init__(self):
        self.table_name = 'iam_api_keys'

    @staticmethod
    def generateCredentials():
        # generate a random string of length 32bytes for the key id
        key_id = os.urandom(32).hex()
        # generate the salt
        salt = os.urandom(32).hex()
        # generate a random string of length 64bytes for the key value
        key_value_row = os.urandom(32).hex()
        # hash the key value with the salt
        key_value_hashed = hashlib.pbkdf2_hmac('sha256', key_value_row.encode('utf-8'), salt.encode('utf-8'), 100000).hex()

        return key_id, salt, key_value_row, key_value_hashed

    def create(self, payload: dict):
        data = payload['data']
        db = payload['db']
        user = payload['user']

        if user['type'] != 'user':
            return {'error': 'Only users can create api keys'}, 400

        key_id, salt, key_value_row, key_value_hashed = self.generateCredentials()

        # add validation
        if data.get('key_group') is None or data.get('key_rate_limit') is None:
            return {'error': 'Missing required fields'}, 400

        # insert row into table
        row = {
            'key_id': key_id,
            'key_value': key_value_hashed,
            'key_salt': salt,
            'key_group': data['key_group'],
            'key_owner': user['id'],
            'key_rate_limit': data['key_rate_limit'],
            'key_last_time_used': datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        }

        success, results = db.insert_row(table_name=self.table_name, row=row)

        if not success:
            return {'error': results}, 400

        credentials = {
            'key_id': key_id,
            'key_value': key_value_row
        }

        return credentials, 200

    def read(self, payload: dict):
        data = payload['data']
        db = payload['db']

        # add validation
        if data.get('key_id') is None:
            return {'error': 'Missing required fields'}, 400

        # get row from table
        conditions = {'key_id': data['key_id']}
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
            user.pop('key_value')
            user.pop('key_salt')

        return results, 200

    def delete(self, payload: dict):
        data = payload['data']
        db = payload['db']

        # add validation
        if data.get('key_id') is None:
            return {'error': 'Missing required fields'}, 400

        # delete row from table
        conditions = {'key_id': data['key_id']}
        success, results = db.delete_row(table_name=self.table_name, where_items=conditions)

        if not success:
            return {'error': results}, 400

        return results, 200

    def validate(self, payload: dict):
        data = payload['data']
        db = payload['db']

        # add validation
        if data.get('key_id') is None or data.get('key_value') is None:
            return {'error': 'Missing required fields'}, 400

        try:
            success, apikey = db.get_row(table_name=self.table_name, where_items={'key_id': data['key_id']})
            if not success:
                return {'error': apikey}, 400

            # hash the key value with the salt
            key_value_hashed = hashlib.pbkdf2_hmac('sha256', data['key_value'].encode('utf-8'),
                                                   apikey['key_salt'].encode('utf-8'), 100000).hex()

            if key_value_hashed == apikey['key_value']:
                success, results = db.update_row(table_name=self.table_name, row={'key_last_time_used': datetime.now().strftime("%m/%d/%Y %H:%M:%S")},
                                                 where_items={'key_id': data['key_id']})
                if not success:
                    return {'error': results}, 400

                return True, 200
            else:
                return {'error': 'Invalid api key'}, 400
        except Exception as e:
            return {'error': e}, 400


