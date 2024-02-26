from server.services.customers.models.sub_client_model import SubClientModel
from server.services.customers.models.aws_account_model import AwsAccountModel
from sqlalchemy.orm import Session


class AwsAccount:
    def __init__(self):
        pass

    def createAwsAccount(self, payload: dict):
        data = payload['data']
        db = payload['db']

        # add validation

        with Session(db.engine) as session:
            # check if sub client exists
            sub_client = session.query(SubClientModel).filter_by(Sub_Client_ID=data['Sub_Client_ID']).first()
            if not sub_client:
                return {'error': 'Sub Client does not exist'}, 400


            try:
                aws_account = AwsAccountModel(
                    Account_ID=data['Account_ID'],
                    Sub_Client_ID=data['Sub_Client_ID'],
                    Name=data['Name'],
                    Master_Account=data['Master_Account'],
                    region=data['region']
                )

                session.add(aws_account)
                session.commit()
                return aws_account.to_dict(), 200
            except Exception as e:
                print(e)
                return {'error': 'Failed to create Aws Account'}, 400

    def getAwsAccount(self, payload: dict):
        data = payload['data']
        db = payload['db']

        # add validation

        with Session(db.engine) as session:
            try:
                aws_account = session.query(AwsAccountModel).filter_by(Account_ID=data['Account_ID']).first().to_dict()
                aws_account['Sub_Client_Name'] = session.query(SubClientModel).filter_by(Sub_Client_ID=aws_account['Sub_Client_ID']).first().Name

            except Exception as e:
                print(e)
                return {'error': 'Failed to get Aws Account'}, 400


        return aws_account, 200

    def getAwsAccounts(self, payload: dict):
        db = payload['db']

        with Session(db.engine) as session:
            try:
                aws_accounts = session.query(AwsAccountModel).all()
                aws_accounts = [aws_account.to_dict() for aws_account in aws_accounts]

                for aws_account in aws_accounts:
                    aws_account['Sub_Client_Name'] = session.query(SubClientModel).filter_by(Sub_Client_ID=aws_account['Sub_Client_ID']).first().Name

            except Exception as e:
                print(e)
                return {'error': 'Failed to get Aws Accounts'}, 400

        return aws_accounts, 200

    def updateAwsAccount(self, payload: dict):
        data = payload['data']
        db = payload['db']

        # add validation

        with Session(db.engine) as session:
            try:
                # get sub client ID from sub client name
                sub_client = session.query(SubClientModel).filter_by(Name=data['Sub_Client_Name']).first()
                aws_account = session.query(AwsAccountModel).filter_by(Account_ID=data['Account_ID']).first()
                aws_account.Sub_Client_ID = sub_client.Sub_Client_ID
                aws_account.Name = data['Name']
                aws_account.Master_Account = data['Master_Account']
                aws_account.region = data['region']

                session.commit()
                return aws_account.to_dict(), 200
            except Exception as e:
                print(e)
                return {'error': 'Failed to update Aws Account'}, 400

    def deleteAwsAccount(self, payload: dict):
        data = payload['data']
        db = payload['db']

        # add validation

        with Session(db.engine) as session:
            try:
                aws_account = session.query(AwsAccountModel).filter_by(Account_ID=data['Account_ID']).first()
                session.delete(aws_account)
                session.commit()
            except Exception as e:
                print(e)
                return {'error': 'Failed to delete Aws Account'}, 400

        return {}, 200




