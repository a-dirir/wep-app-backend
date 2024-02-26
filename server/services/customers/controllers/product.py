from server.services.customers.models.product_model import ProductModel
from sqlalchemy.orm import Session


class Product:
    def __init__(self):
        pass

    def createProduct(self, payload: dict):
        data = payload['data']
        db = payload['db']

        # add validation

        with Session(db.engine) as session:
            try:
                product = ProductModel(
                    Product_ID=data['Product_ID'],
                    Name=data['Name'],
                    Product_Type=data['Product_Type']
                )

                session.add(product)
                session.commit()
            except Exception as e:
                print(e)
                return {'error': 'Failed to create Product'}, 400


        return {}, 200

    def getProduct(self, payload: dict):
        data = payload['data']
        db = payload['db']

        # add validation

        with Session(db.engine) as session:
            try:
                product = session.query(ProductModel).filter_by(Product_ID=data['Product_ID']).first().to_dict()
            except Exception as e:
                print(e)
                return {'error': 'Failed to get Product'}, 400


        return product, 200

    def getProducts(self, payload: dict):
        db = payload['db']

        with Session(db.engine) as session:
            try:
                products = session.query(ProductModel).all()
                products = [product.to_dict() for product in products]
            except Exception as e:
                print(e)
                return {'error': 'Failed to get Products'}, 400

        return products, 200

    def updateProduct(self, payload: dict):
        data = payload['data']
        db = payload['db']

        # add validation

        with Session(db.engine) as session:
            try:
                product = session.query(ProductModel).filter_by(Product_ID=data['Product_ID']).first()

                product.Name = data['Name']
                product.Product_Type = data['Product_Type']

                session.commit()
            except Exception as e:
                print(e)
                return {'error': 'Failed to update Product'}, 400

        return {}, 200

    def deleteProduct(self, payload: dict):
        data = payload['data']
        db = payload['db']

        # add validation

        with Session(db.engine) as session:
            try:
                product = session.query(ProductModel).filter_by(Product_ID=data['Product_ID']).first()

                session.delete(product)
                session.commit()
            except Exception as e:
                print(e)
                return {'error': 'Failed to delete Product'}, 400

        return {}, 200




