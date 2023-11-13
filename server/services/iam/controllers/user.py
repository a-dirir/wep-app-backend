from server.services.iam.models.iam_models import UserModel
from sqlalchemy.orm import Session


class User:
    def __init__(self):
        pass

    def createUser(self, payload: dict):
        data = payload['data']
        db = payload['db']

        # add validation

        with Session(db.engine) as session:
            try:
                user = UserModel(
                    email=data['email'],
                    name=data['name'],
                    group=data['group']
                )

                session.add(user)
                session.commit()
            except Exception as e:
                print(e)
                return {'error': 'Failed to create User'}, 400

        return {}, 200

    def getUser(self, payload: dict):
        data = payload['data']
        db = payload['db']

        # add validation

        with Session(db.engine) as session:
            try:
                user = session.query(UserModel).filter_by(email=data['email']).first().to_dict()
            except Exception as e:
                print(e)
                return {'error': 'Failed to get User'}, 400
        
        return user, 200

    def getUsers(self, payload: dict):
        db = payload['db']

        with Session(db.engine) as session:
            try:
                users = session.query(UserModel).all()
                users = [user.to_dict() for user in users]
            except Exception as e:
                print(e)
                return {'error': 'Failed to get Users'}, 400

        return users, 200

    def updateUser(self, payload: dict):
        data = payload['data']
        db = payload['db']

        # add validation

        with Session(db.engine) as session:
            try:
                user = session.query(UserModel).filter_by(email=data['email']).first()
                user.name = data['name']
                user.group = data['group']
                session.commit()
            except Exception as e:
                print(e)
                return {'error': 'Failed to update User'}, 400


        return {}, 200

    def deleteUser(self, payload: dict):
        data = payload['data']
        db = payload['db']

        # add validation

        with Session(db.engine) as session:
            try:
                user = session.query(UserModel).filter_by(email=data['email']).first()
                session.delete(user)
                session.commit()
            except Exception as e:
                print(e)
                return {'error': 'Failed to delete User'}, 400
        
        return {}, 200





