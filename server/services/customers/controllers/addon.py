from server.services.customers.models.addon_model import AddonModel
from sqlalchemy.orm import Session


class Addon:
    def __init__(self):
        pass

    def createAddon(self, payload: dict):
        data = payload['data']
        db = payload['db']

        # add validation

        with Session(db.engine) as session:
            try:
                addon = AddonModel(
                    Addon_ID=data['Addon_ID'],
                    Name=data['Name'],
                    Addon_Type=data['Addon_Type']
                )

                session.add(addon)
                session.commit()
            except Exception as e:
                print(e)
                return {'error': 'Failed to create Addon'}, 400


        return {}, 200

    def getAddon(self, payload: dict):
        data = payload['data']
        db = payload['db']

        # add validation

        with Session(db.engine) as session:
            try:
                addon = session.query(AddonModel).filter_by(Addon_ID=data['Addon_ID']).first().to_dict()
            except Exception as e:
                print(e)
                return {'error': 'Failed to get Addon'}, 400


        return addon, 200

    def getAddons(self, payload: dict):
        db = payload['db']

        with Session(db.engine) as session:
            try:
                addons = session.query(AddonModel).all()
                addons = [addon.to_dict() for addon in addons]
            except Exception as e:
                print(e)
                return {'error': 'Failed to get Addons'}, 400

        return addons, 200

    def updateAddon(self, payload: dict):
        data = payload['data']
        db = payload['db']

        # add validation

        with Session(db.engine) as session:
            try:
                addon = session.query(AddonModel).filter_by(Addon_ID=data['Addon_ID']).first()

                addon.Name = data['Name']
                addon.Addon_Type = data['Addon_Type']

                session.commit()
            except Exception as e:
                print(e)
                return {'error': 'Failed to update Addon'}, 400

        return {}, 200

    def deleteAddon(self, payload: dict):
        data = payload['data']
        db = payload['db']

        # add validation

        with Session(db.engine) as session:
            try:
                addon = session.query(AddonModel).filter_by(Addon_ID=data['Addon_ID']).first()

                session.delete(addon)
                session.commit()
            except Exception as e:
                print(e)
                return {'error': 'Failed to delete Addon'}, 400

        return {}, 200




