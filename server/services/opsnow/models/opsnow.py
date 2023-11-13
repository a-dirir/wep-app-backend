from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.mysql import JSON
from server.database.mysqlDB import Base


class OPSNOWCustomerModel(Base):
    __tablename__ = "opsnow_customers"
    customer_id = Column(String(128), ForeignKey("iam_customer.id"), primary_key=True)
    cmpnId = Column(String(128), nullable=False)
    cmpnNm = Column(String(256), nullable=False)
    vendor = Column(JSON, nullable=False)

    def __repr__(self):
        return f"<Customer(customer_id={self.customer_id}, cmpnId={self.cmpnId}, cmpnNm={self.cmpnNm})>"

    def to_dict(self):
        return {
            "customer_id": self.customer_id,
            "cmpnId": self.cmpnId,
            "cmpnNm": self.cmpnNm,
            "vendor": self.vendor,
        }


class AssetsModel(Base):
    __tablename__ = "opsnow_assets"
    customer_id = Column(String(128), ForeignKey("iam_customer.id"), primary_key=True)
    cmpnId = Column(String(128), nullable=False)
    cmpnNm = Column(String(256), nullable=False)
    usage = Column(JSON, nullable=False)
    products = Column(JSON, nullable=False)
    resources = Column(JSON, nullable=False)


    def __repr__(self):
        return f"<Assets(cmpnId={self.cmpnId}, cmpnNm={self.cmpnNm})>"

    def to_dict(self):
        return {
            "customer_id": self.customer_id,
            "cmpnId": self.cmpnId,
            "cmpnNm": self.cmpnNm,
            "usage": self.usage,
            "products": self.products,
            "resources": self.resources,
        }