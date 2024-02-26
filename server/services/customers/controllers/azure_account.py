from server.services.customers.models.sub_client_model import SubClientModel
from server.services.customers.models.azure_account_model import AzureAccountModel
from sqlalchemy.orm import Session


class AzureAccount:
    def __init__(self):
        pass

    def createAzureAccount(self, payload: dict):
        data = payload['data']
        db = payload['db']

        # add validation

        with Session(db.engine) as session:
            try:
                # check if sub client exists
                sub_client = session.query(SubClientModel).filter_by(Sub_Client_ID=data['Sub_Client_ID']).first()
                if not sub_client:
                    return {'error': 'Sub Client does not exist'}, 400

                azure_account = AzureAccountModel(
                    Subscription_ID=data['Subscription_ID'],
                    Sub_Client_ID=data['Sub_Client_ID'],
                    Name=data['Name'],
                    Tenant_ID=data['Tenant_ID']
                )

                session.add(azure_account)
                session.commit()
                return azure_account.to_dict(), 200
            except Exception as e:
                print(e)
                return {'error': 'Failed to create Azure Account'}, 400

    def getAzureAccount(self, payload: dict):
        data = payload['data']
        db = payload['db']

        # add validation

        with Session(db.engine) as session:
            try:
                azure_account = session.query(AzureAccountModel).filter_by(Subscription_ID=data['Subscription_ID']).first().to_dict()
                azure_account['Sub_Client_Name'] = session.query(SubClientModel).filter_by(Sub_Client_ID=azure_account['Sub_Client_ID']).first().Name
            except Exception as e:
                print(e)
                return {'error': 'Failed to get Azure Account'}, 400


        return azure_account, 200

    def getAzureAccounts(self, payload: dict):
        db = payload['db']

        with Session(db.engine) as session:
            try:
                azure_accounts = session.query(AzureAccountModel).all()
                azure_accounts = [azure_account.to_dict() for azure_account in azure_accounts]

                for azure_account in azure_accounts:
                    azure_account['Sub_Client_Name'] = session.query(SubClientModel).filter_by(Sub_Client_ID=azure_account['Sub_Client_ID']).first().Name

            except Exception as e:
                print(e)
                return {'error': 'Failed to get Azure Accounts'}, 400

        return azure_accounts, 200

    def updateAzureAccount(self, payload: dict):
        data = payload['data']
        db = payload['db']

        # add validation

        with Session(db.engine) as session:
            try:
                # get sub client ID from sub client name
                sub_client = session.query(SubClientModel).filter_by(Name=data['Sub_Client_Name']).first()
                azure_account = session.query(AzureAccountModel).filter_by(Subscription_ID=data['Subscription_ID']).first()
                azure_account.Sub_Client_ID = sub_client.Sub_Client_ID
                azure_account.Name = data['Name']
                azure_account.Tenant_ID = data['Tenant_ID']


                session.commit()
                return azure_account.to_dict(), 200
            except Exception as e:
                print(e)
                return {'error': 'Failed to update Azure Account'}, 400

    def deleteAzureAccount(self, payload: dict):
        data = payload['data']
        db = payload['db']

        # add validation

        with Session(db.engine) as session:
            try:
                azure_account = session.query(AzureAccountModel).filter_by(Subscription_ID=data['Subscription_ID']).first()
                session.delete(azure_account)
                session.commit()
            except Exception as e:
                print(e)
                return {'error': 'Failed to delete Azure Account'}, 400

        return {}, 200




