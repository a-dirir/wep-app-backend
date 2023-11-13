from server.services.iam.models.iam_models import GroupModel
from sqlalchemy.orm import Session


class Group:
    def __init__(self):
        pass

    def createGroup(self, payload: dict):
        data = payload['data']
        db = payload['db']

        # add validation

        with Session(db.engine) as session:
            try:
                group = GroupModel(
                    name=data['name'],
                    description=data['description'],
                    policy=data['policy']
                )

                session.add(group)
                session.commit()
            except Exception as e:
                print(e)
                return {'error': 'Failed to create Group'}, 400


        return {}, 200

    def getGroup(self, payload: dict):
        data = payload['data']
        db = payload['db']

        # add validation

        with Session(db.engine) as session:
            try:
                group = session.query(GroupModel).filter_by(name=data['name']).first().to_dict()
            except Exception as e:
                print(e)
                return {'error': 'Failed to get Group'}, 400


        return group, 200

    def getGroups(self, payload: dict):
        db = payload['db']

        with Session(db.engine) as session:
            try:
                groups = session.query(GroupModel).all()
                groups = [group.to_dict() for group in groups]
            except Exception as e:
                print(e)
                return {'error': 'Failed to get Groups'}, 400

        return groups, 200

    def updateGroup(self, payload: dict):
        data = payload['data']
        db = payload['db']

        # add validation

        with Session(db.engine) as session:
            try:
                group = session.query(GroupModel).filter_by(name=data['name']).first()

                group.description = data['description']
                group.policy = data['policy']

                session.commit()
            except Exception as e:
                print(e)
                return {'error': 'Failed to update Group'}, 400

        return {}, 200

    def deleteGroup(self, payload: dict):
        data = payload['data']
        db = payload['db']

        # add validation

        with Session(db.engine) as session:
            try:
                group = session.query(GroupModel).filter_by(name=data['name']).first()

                session.delete(group)
                session.commit()
            except Exception as e:
                print(e)
                return {'error': 'Failed to delete Group'}, 400

        return {}, 200




