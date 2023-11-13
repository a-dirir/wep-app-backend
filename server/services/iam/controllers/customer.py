from server.services.iam.models.iam_models import IAMCustomerModel
from sqlalchemy.orm import Session


class Customer:
    def __init__(self):
        pass

    def getCustomers(self, payload: dict):
        db = payload['db']

        with Session(db.engine) as session:
            try:
                customers = session.query(IAMCustomerModel).all()
                return {'customers': [customer.to_dict() for customer in customers]}, 200
            except Exception as e:
                print(e)
                return {'error': 'Failed to get customers'}, 400

    def getCustomer(self, payload: dict):
        db = payload['db']
        customer_id = payload['customer_id']

        with Session(db.engine) as session:
            try:
                customer = session.query(IAMCustomerModel).filter(id=customer_id).first().to_dict()
                return customer, 200
            except Exception as e:
                print(e)
                return {'error': 'Failed to get customer'}, 400

    def createCustomer(self, payload: dict):
        db = payload['db']
        data = payload['data']

        with Session(db.engine) as session:
            try:
                customer = IAMCustomerModel(
                    id=data['id'],
                    name=data['name'],
                    config=data['config']
                )

                session.add(customer)
                session.commit()
                return {}, 200
            except Exception as e:
                print(e)
                return {'error': 'Failed to create customer'}, 400

    def updateCustomer(self, payload: dict):
        db = payload['db']
        data = payload['data']
        customer_id = payload['customer_id']

        with Session(db.engine) as session:
            try:
                customer = session.query(IAMCustomerModel).filter(id=customer_id).first()
                customer.name = data['name']
                customer.config = data['config']
                session.commit()
                return {}, 200
            except Exception as e:
                print(e)
                return {'error': 'Failed to update customer'}, 400

    def deleteCustomer(self, payload: dict):
        db = payload['db']
        customer_id = payload['customer_id']

        with Session(db.engine) as session:
            try:
                customer = session.query(IAMCustomerModel).filter(id=customer_id).first()
                session.delete(customer)
                session.commit()
                return {}, 200
            except Exception as e:
                print(e)
                return {'error': 'Failed to delete customer'}, 400
