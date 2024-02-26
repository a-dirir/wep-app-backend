from server.services.customers.models.sub_client_model import SubClientModel
from server.services.customers.models.synthetic_model import SyntheticModel
from sqlalchemy.orm import Session


class Synthetic:
    def __init__(self):
        pass

    def createSynthetic(self, payload: dict):
        data = payload['data']
        db = payload['db']

        # add validation

        # get only date in format YYYY-MM-DD, add one day to the date
        data['URL_SSL_Expiry_Date'] = data['URL_SSL_Expiry_Date'].split('T')[0]

        with Session(db.engine) as session:
            try:
                synthetic = SyntheticModel(
                    Sub_Client_ID=data['Sub_Client_ID'],
                    URL=data['URL'],
                    URL_SSL_Expiry_Date=data['URL_SSL_Expiry_Date']
                )

                session.add(synthetic)
                session.commit()
                return synthetic.to_dict(), 200
            except Exception as e:
                print(e)
                return {'error': 'Failed to create Synthetic'}, 400

    def getSynthetic(self, payload: dict):
        data = payload['data']
        db = payload['db']

        # add validation

        with Session(db.engine) as session:
            try:
                synthetic = session.query(SyntheticModel).filter_by(URL=data['URL']).first().to_dict()
                synthetic['Sub_Client_Name'] = session.query(SubClientModel).filter_by(Sub_Client_ID=synthetic['Sub_Client_ID']).first().Name
            except Exception as e:
                print(e)
                return {'error': 'Failed to get Synthetic'}, 400


        return synthetic, 200

    def getSynthetics(self, payload: dict):
        db = payload['db']

        with Session(db.engine) as session:
            try:
                synthetics = session.query(SyntheticModel).all()
                synthetics = [synthetic.to_dict() for synthetic in synthetics]

                # add sub client name to synthetic
                for synthetic in synthetics:
                    synthetic['Sub_Client_Name'] = session.query(SubClientModel).filter_by(Sub_Client_ID=synthetic['Sub_Client_ID']).first().Name

            except Exception as e:
                print(e)
                return {'error': 'Failed to get Synthetics'}, 400

        return synthetics, 200

    def updateSynthetic(self, payload: dict):
        data = payload['data']
        db = payload['db']

        # add validation

        with Session(db.engine) as session:
            try:
                synthetic = session.query(SyntheticModel).filter_by(URL=data['URL']).first()
                # get only date in format YYYY-MM-DD
                data['URL_SSL_Expiry_Date'] = data['URL_SSL_Expiry_Date'].split('T')[0]
                synthetic.URL_SSL_Expiry_Date = data['URL_SSL_Expiry_Date']
                session.commit()
                return synthetic.to_dict(), 200
            except Exception as e:
                print(e)
                return {'error': 'Failed to update Synthetic'}, 400

    def deleteSynthetic(self, payload: dict):
        data = payload['data']
        db = payload['db']

        # add validation

        with Session(db.engine) as session:
            try:
                synthetic = session.query(SyntheticModel).filter_by(URL=data['URL']).first()
                session.delete(synthetic)
                session.commit()
            except Exception as e:
                print(e)
                return {'error': 'Failed to delete Synthetic'}, 400

        return {}, 200




