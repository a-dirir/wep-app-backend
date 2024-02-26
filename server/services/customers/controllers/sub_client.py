from server.services.customers.models.client_model import ClientModel
from server.services.customers.models.sub_client_model import SubClientModel
from sqlalchemy.orm import Session


class SubClient:
    def __init__(self):
        pass

    def createSubClient(self, payload: dict):
        data = payload['data']
        db = payload['db']

        # add validation

        with Session(db.engine) as session:
            sub_client_name = data['Name']
            # check if length of client name is less than 10
            if len(sub_client_name) < 9:
                return {'error': 'Sub Client name should be at least 9 characters long'}, 400

            # generate client id from client name by taking the first and last 5 characters
            sub_client_id = sub_client_name[:5] + "-" + sub_client_name[-4:]

            # check if sub client ID already exists
            sub_client = session.query(SubClientModel).filter_by(Sub_Client_ID=sub_client_id).first()
            if sub_client:
                return {'error': 'Sub Client ID already exists, try chaning name'}, 400


            # check if client id already exists
            client = session.query(ClientModel).filter_by(Client_ID=data['Client_ID']).first()

            if not client:
                return {'error': 'Client ID does not exist'}, 400

            # extract date from first engagement date string
            data['First_Engagement_Date'] = data['First_Engagement_Date'].split('T')[0]


            # find engagement year and quarter from first engagement date string
            engagement_year = data['First_Engagement_Date'].split('-')[0]
            engagement_quarter = f"Q{int(data['First_Engagement_Date'].split('-')[1]) // 3 + 1}-{engagement_year}"

            try:
                sub_client = SubClientModel(
                    Sub_Client_ID=sub_client_id,
                    Name=data['Name'],
                    Status="Current",
                    Client_ID=data['Client_ID'],
                    First_Engagement_Date=data['First_Engagement_Date'],
                    Engagement_Year=engagement_year,
                    Engagement_Quarter=engagement_quarter
                )

                session.add(sub_client)
                session.commit()
            except Exception as e:
                print(e)
                return {'error': 'Failed to create SubClient'}, 400


        return {}, 200

    def getSubClient(self, payload: dict):
        data = payload['data']
        db = payload['db']

        # add validation

        with Session(db.engine) as session:
            try:
                sub_client = session.query(SubClientModel).filter_by(Sub_Client_ID=data['Sub_Client_ID']).first().to_dict()
            except Exception as e:
                print(e)
                return {'error': 'Failed to get Sub Client'}, 400


        return sub_client, 200

    def getSubClients(self, payload: dict):
        db = payload['db']

        with Session(db.engine) as session:
            try:
                sub_clients = session.query(SubClientModel).all()
                sub_clients = [sub_client.to_dict() for sub_client in sub_clients]

                # add client name to sub client
                for sub_client in sub_clients:
                    sub_client['Client_Name'] = session.query(ClientModel).filter_by(Client_ID=sub_client['Client_ID']).first().Name
                    # convert first engagement date to string
                    sub_client['First_Engagement_Date'] = sub_client['First_Engagement_Date'].strftime("%Y-%m-%d")

            except Exception as e:
                print(e)
                return {'error': 'Failed to get Sub Clients'}, 400
        print(sub_clients)
        return sub_clients, 200

    def updateSubClient(self, payload: dict):
        data = payload['data']
        db = payload['db']

        # add validation

        with Session(db.engine) as session:
            try:
                sub_client = session.query(SubClientModel).filter_by(Sub_Client_ID=data['Sub_Client_ID']).first()

                # check if client id already exists
                client = session.query(ClientModel).filter_by(Client_ID=data['Client_ID']).first()
                if not client:
                    return {'error': 'Client ID does not exist'}, 400

                sub_client.Client_ID = data['Client_ID']

                # extract date from first engagement date string,
                # and find engagement year and quarter from first engagement date string
                data['First_Engagement_Date'] = data['First_Engagement_Date'].split('T')[0]
                engagement_year = data['First_Engagement_Date'].split('-')[0]
                engagement_quarter = f"Q{int(data['First_Engagement_Date'].split('-')[1]) // 3 + 1}-{engagement_year}"
                sub_client.First_Engagement_Date = data['First_Engagement_Date']
                sub_client.Engagement_Year = engagement_year
                sub_client.Engagement_Quarter = engagement_quarter

                session.commit()

                return sub_client.to_dict(), 200
            except Exception as e:
                print(e)
                return {'error': 'Failed to update Sub Client'}, 400



    def deleteSubClient(self, payload: dict):
        data = payload['data']
        db = payload['db']

        # add validation

        with Session(db.engine) as session:
            try:
                sub_client = session.query(SubClientModel).filter_by(Sub_Client_ID=data['Sub_Client_ID']).first()
                session.delete(sub_client)
                session.commit()
            except Exception as e:
                print(e)
                return {'error': 'Failed to delete Sub Client'}, 400

        return {}, 200




