from server.services.customers.models.sub_client_model import SubClientModel
from server.services.customers.models.m365_account_model import M365AccountModel
from sqlalchemy.orm import Session


class M365Account:
    def __init__(self):
        pass

    def createM365Account(self, payload: dict):
        data = payload['data']
        db = payload['db']

        # add validation

        with Session(db.engine) as session:
            # check if sub client exists
            sub_client = session.query(SubClientModel).filter_by(Sub_Client_ID=data['Sub_Client_ID']).first()
            if not sub_client:
                return {'error': 'Sub Client does not exist'}, 400

            try:
                m365_account = M365AccountModel(
                    Sub_Client_ID=data['Sub_Client_ID'],
                    Name=data['Name'],
                    Tenant_ID=data['Tenant_ID']
                )

                session.add(m365_account)
                session.commit()
                return m365_account.to_dict(), 200
            except Exception as e:
                print(e)
                return {'error': 'Failed to create M365 Account'}, 400

    def getM365Account(self, payload: dict):
        data = payload['data']
        db = payload['db']

        # add validation

        with Session(db.engine) as session:
            try:
                m365_account = session.query(M365AccountModel).filter_by(Tenant_ID=data['Tenant_ID']).first().to_dict()
                m365_account['Sub_Client_Name'] = session.query(SubClientModel).filter_by(Sub_Client_ID=m365_account['Sub_Client_ID']).first().Name
            except Exception as e:
                print(e)
                return {'error': 'Failed to get M365 Account'}, 400


        return m365_account, 200

    def getM365Accounts(self, payload: dict):
        db = payload['db']

        with Session(db.engine) as session:
            try:
                m365_accounts = session.query(M365AccountModel).all()
                m365_accounts = [m365_account.to_dict() for m365_account in m365_accounts]

                for m365_account in m365_accounts:
                    m365_account['Sub_Client_Name'] = session.query(SubClientModel).filter_by(Sub_Client_ID=m365_account['Sub_Client_ID']).first().Name

            except Exception as e:
                print(e)
                return {'error': 'Failed to get M365 Accounts'}, 400

        return m365_accounts, 200

    def updateM365Account(self, payload: dict):
        data = payload['data']
        db = payload['db']

        # add validation

        with Session(db.engine) as session:
            try:
                # get sub client ID from sub client name
                sub_client = session.query(SubClientModel).filter_by(Name=data['Sub_Client_Name']).first()
                m365_account = session.query(M365AccountModel).filter_by(Tenant_ID=data['Tenant_ID']).first()
                m365_account.Sub_Client_ID = sub_client.Sub_Client_ID
                m365_account.Name = data['Name']
                session.commit()
                return m365_account.to_dict(), 200
            except Exception as e:
                print(e)
                return {'error': 'Failed to update M365 Account'}, 400

    def deleteM365Account(self, payload: dict):
        data = payload['data']
        db = payload['db']

        # add validation

        with Session(db.engine) as session:
            try:
                m365_account = session.query(M365AccountModel).filter_by(Tenant_ID=data['Tenant_ID']).first()
                session.delete(m365_account)
                session.commit()
            except Exception as e:
                print(e)
                return {'error': 'Failed to delete M365 Account'}, 400

        return {}, 200




