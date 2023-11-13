from sqlalchemy.orm import Session

from server.services.iam.models.iam_models import IAMCustomerModel
from server.services.opsnow.models.opsnow import OPSNOWCustomerModel
from server.services.opsnow.controllers.connector import OpsNowConnector


class Customers:
    def __init__(self):
        self.opsnow_connector = OpsNowConnector()

    def loadCustomers(self, payload: dict):
        db = payload['db']

        # load iam customers
        with Session(db.engine) as session:
            try:
                iam_customers = session.query(IAMCustomerModel).all()
                iam_customers = [customer.to_dict() for customer in iam_customers]
            except Exception as e:
                print(e)
                return {'error': 'Failed to load customers'}, 400

        opsnow_customers = self.opsnow_connector.get_company_list()['result']['cmpnList']
        with Session(db.engine) as session:
            try:
                for opsnow_customer in opsnow_customers:

                    for iam_customer in iam_customers:
                        if opsnow_customer['cmpnId'] == iam_customer['config']['opsnowid']:
                            session.add(
                                OPSNOWCustomerModel(
                                    customer_id=iam_customer['id'],
                                    cmpnId=opsnow_customer['cmpnId'],
                                    cmpnNm=opsnow_customer['cmpnNm'],
                                    vendor=opsnow_customer['vendor']
                                )
                            )
                            break


                session.commit()
            except Exception as e:
                print(e)
                return {'error': 'Failed to load customers'}, 400

        return {}, 200

    def getCustomers(self, payload: dict):
        db = payload['db']

        with Session(db.engine) as session:
            try:
                opsnow_customers = session.query(OPSNOWCustomerModel).all()
                return {'opsnow_customers': [opsnow_customer.to_dict() for opsnow_customer in opsnow_customers]}, 200
            except Exception as e:
                print(e)
                return {'error': 'Failed to get customers'}, 400
