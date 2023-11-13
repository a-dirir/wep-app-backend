import hashlib
from datetime import datetime

from server.services.iam.models.iam_models import APIKeyModel
from sqlalchemy.orm import Session
import os


class ApiKey:
    def __init__(self):
        pass

    @staticmethod
    def generateApiKey():
        # generate a random string of length 32bytes for the key id
        key_id = os.urandom(32).hex()
        # generate the salt
        salt = os.urandom(32).hex()
        # generate a random string of length 64bytes for the key value
        key_value_row = os.urandom(32).hex()
        # hash the key value with the salt
        key_value_hashed = hashlib.pbkdf2_hmac('sha256', key_value_row.encode('utf-8'), salt.encode('utf-8'), 100000).hex()

        return key_id, salt, key_value_row, key_value_hashed

    def createApiKey(self, payload: dict):
        data = payload['data']
        db = payload['db']
        user = payload['user']

        if user['type'] != 'user':
            return {'error': 'Only users can create api keys'}, 400

        key_id, salt, key_value_row, key_value_hashed = self.generateApiKey()
        # add validation

        with Session(db.engine) as session:
            try:
                apikey = APIKeyModel(
                    key_id=key_id,
                    key_value=key_value_hashed,
                    key_salt=salt,
                    key_group=data['key_group'],
                    key_owner=user['id'],
                    key_rate_limit=data['key_rate_limit'],
                    key_last_time_used=datetime.now()
                )

                session.add(apikey)
                session.commit()

            except Exception as e:
                print(e)
                return {'error': 'Failed to create api key'}, 400

        return {
            'key_id': key_id,
            'key_value': key_value_row,
            'key_group': data['key_group'],
            'key_owner': user['id'],
            'key_rate_limit': data['key_rate_limit'],
            'key_last_time_used': datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        }, 200

    def getApiKey(self, payload: dict):
        data = payload['data']
        db = payload['db']

        # add validation

        with Session(db.engine) as session:
            try:
                apikey = session.query(APIKeyModel).filter_by(key_id=data['key_id']).first().to_dict()
                apikey.pop('key_value')
                apikey.pop('key_salt')
            except Exception as e:
                print(e)
                return {'error': 'Failed to get api key'}, 400

        return apikey, 200

    def getApiKeys(self, payload: dict):
        db = payload['db']


        with Session(db.engine) as session:
            try:
                # get all api keys, but don't return the key_value or key_salt
                apikeys = session.query(APIKeyModel).all()
                apikeys = [apikey.to_dict() for apikey in apikeys]
                for apikey in apikeys:
                    apikey.pop('key_value')
                    apikey.pop('key_salt')
            except Exception as e:
                print(e)
                return {'error': 'Failed to get api keys'}, 400

        return apikeys, 200

    def updateApiKey(self, payload: dict):
        data = payload['data']
        db = payload['db']

        # add validation

        with Session(db.engine) as session:
            try:
                apikey = session.query(APIKeyModel).filter_by(key_id=data['key_id']).first()
                apikey.key_group = data['key_group']
                apikey.key_rate_limit = data['key_rate_limit']
                session.commit()
            except Exception as e:
                print(e)
                return {'error': 'Failed to update api key'}, 400

        return {}, 200

    def deleteApiKey(self, payload: dict):
        data = payload['data']
        db = payload['db']

        # add validation

        with Session(db.engine) as session:
            try:
                apikey = session.query(APIKeyModel).filter_by(key_id=data['key_id']).first()
                session.delete(apikey)
                session.commit()
            except Exception as e:
                print(e)
                return {'error': 'Failed to delete api key'}, 400

        return {}, 200

    def validateApiKey(self, payload: dict):
        data = payload['data']
        db = payload['db']

        # add validation

        with Session(db.engine) as session:
            try:
                apikey = session.query(APIKeyModel).filter_by(key_id=data['key_id']).first()
                # hash the key value with the salt
                key_value_hashed = hashlib.pbkdf2_hmac('sha256', data['key_value'].encode('utf-8'), apikey.key_salt.encode('utf-8'), 100000).hex()
                if key_value_hashed == apikey.key_value:
                    apikey.key_last_time_used = datetime.now()
                    session.commit()
                    return {}, 200
                else:
                    return {'error': 'Invalid api key'}, 400
            except Exception as e:
                print(e)
                return {'error': 'Failed to validate api key'}, 400


