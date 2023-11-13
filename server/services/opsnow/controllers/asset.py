import time
from sqlalchemy.orm import Session

from server.services.opsnow.models.opsnow import OPSNOWCustomerModel, AssetsModel
from server.services.opsnow.controllers.connector import OpsNowConnector


class Asset:
    def __init__(self):
        self.opsnow_connector = OpsNowConnector()

    def loadAssets(self, payload: dict):
        db = payload['db']

        with Session(db.engine) as session:
            try:
                customers = session.query(OPSNOWCustomerModel).all()
                customers = [customer.to_dict() for customer in customers]
            except Exception as e:
                print(e)
                return {'error': 'Failed to load customers'}, 400

        now = time.time()

        for customer in customers:
            customer_id = customer['customer_id']
            cmpnId = customer['cmpnId']
            cmpnNm = customer['cmpnNm']
            vendors = customer['vendor']
            self.opsnow_connector.set_current_company(cmpnId)

            usage = self.opsnow_connector.get_usage()['result']
            all_prodcuts = []
            resources = []
            for vendor in vendors:
                vendor_id = vendor['cloudVndrId']
                accounts = [account['accId'] for account in vendor['accountList']]

                if vendor_id == 'azu':
                    vendor_id = 'azure'
                    products = self.opsnow_connector.get_total_user_product_azure(accounts)
                else:
                    products = self.opsnow_connector.get_total_user_product_aws(accounts)

                products = {
                    'type': 'products',
                    'vendor': vendor_id,
                    'products_counts': products['result']['rsrcList']
                }

                all_prodcuts.append(products)

                resources = []

                for resource in usage['products']:
                    if resource['vndr'] != vendor_id:
                        continue

                    resource_id = resource['key']
                    resource_items = self.opsnow_connector.get_resource_usage(resource_id=resource_id, provider=vendor_id)
                    resource_items['type'] = f"{vendor_id}_{resource_id}"
                    resources.append(resource_items)

            with Session(db.engine) as session:
                try:
                    session.add(
                        AssetsModel(
                            customer_id=customer_id,
                            cmpnId=cmpnId,
                            cmpnNm=cmpnNm,
                            usage=usage,
                            products=all_prodcuts,
                            resources=resources
                        )
                    )

                    session.commit()
                except Exception as e:
                    print(e)
                    return {'error': 'Failed to load assets'}, 400

        print(f"Time taken in loading assets: {time.time() - now}")

        return {}, 200

    def getAssets(self, payload: dict):
        data = payload['data']
        db = payload['db']

        customer_id = data['customer_id']

        with Session(db.engine) as session:
            assets = session.query(AssetsModel).filter_by(customer_id=customer_id).first().to_dict()
            if assets is None:
                return {'error': 'Invalid customer'}, 400

        return assets, 200

    def getProducts(self, payload: dict):
        data = payload['data']
        db = payload['db']

        customer_id = data['customer_id']

        if customer_id == 'Root':
            return {}, 200

        with Session(db.engine) as session:
            assets = session.query(AssetsModel).filter_by(customer_id=customer_id).first().to_dict()
            # remove resources and usage
            assets.pop('resources')
            assets.pop('usage')
            if assets is None:
                return {'error': 'Invalid customer'}, 400

        return assets, 200

    def getResources(self, payload: dict):
        data = payload['data']
        db = payload['db']

        customer_id = data['customer_id']

        if customer_id == 'Root':
            return {}, 200

        with Session(db.engine) as session:
            assets = session.query(AssetsModel).filter_by(customer_id=customer_id).first().to_dict()
            # remove resources and usage
            assets.pop('products')
            assets.pop('usage')
            if assets is None:
                return {'error': 'Invalid customer'}, 400

        return assets, 200

    def getUsage(self, payload: dict):
        data = payload['data']
        db = payload['db']

        customer_id = data['customer_id']

        if customer_id == 'Root':
            return {}, 200

        with Session(db.engine) as session:
            assets = session.query(AssetsModel).filter_by(customer_id=customer_id).first().to_dict()
            # remove resources and usage
            assets.pop('products')
            assets.pop('resources')
            if assets is None:
                return {'error': 'Invalid customer'}, 400

        return assets, 200