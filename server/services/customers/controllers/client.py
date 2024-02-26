from server.services.customers.models.client_model import ClientModel
from sqlalchemy.orm import Session


class Client:
    def __init__(self):
        pass

    def createClient(self, payload: dict):
        data = payload['data']
        db = payload['db']

        # add validation

        with Session(db.engine) as session:
            client_name = data['Name']
            # check if length of client name is less than 10
            if len(client_name) < 9:
                return {'error': 'Client name should be at least 9 characters long'}, 400

            # generate client id from client name by taking the first and last 5 characters
            client_id = client_name[:5] + "-" + client_name[-4:]

            # check if client name already exists
            client = session.query(ClientModel).filter_by(Client_ID=client_id).first()
            if client:
                return {'error': 'Client ID already exists, try changing name'}, 400



            try:
                client = ClientModel(
                    Client_ID=client_id,
                    Name=data['Name']
                )

                session.add(client)
                session.commit()
            except Exception as e:
                print(e)
                return {'error': 'Failed to create Client'}, 400


        return {}, 200

    def getClient(self, payload: dict):
        data = payload['data']
        db = payload['db']

        # add validation

        with Session(db.engine) as session:
            try:
                client = session.query(ClientModel).filter_by(Client_ID=data['Client_ID']).first().to_dict()
            except Exception as e:
                print(e)
                return {'error': 'Failed to get Client'}, 400


        return client, 200

    def getClients(self, payload: dict):
        db = payload['db']

        with Session(db.engine) as session:
            try:
                clients = session.query(ClientModel).all()
                clients = [client.to_dict() for client in clients]
            except Exception as e:
                print(e)
                return {'error': 'Failed to get Clients'}, 400

        return clients, 200

    def updateClient(self, payload: dict):
        data = payload['data']
        db = payload['db']

        return {}, 200

    def deleteClient(self, payload: dict):
        data = payload['data']
        db = payload['db']

        # add validation

        with Session(db.engine) as session:
            try:
                client = session.query(ClientModel).filter_by(Client_ID=data['Client_ID']).first()
                session.delete(client)
                session.commit()
            except Exception as e:
                print(e)
                return {'error': 'Failed to delete Client'}, 400

        return {}, 200




