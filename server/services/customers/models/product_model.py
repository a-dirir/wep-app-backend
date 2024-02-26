from sqlalchemy import Column, String
from server.database.mysqlDB import Base


class ProductModel(Base):
    __tablename__ = "products"
    Product_ID = Column(String(100), primary_key=True)
    Name = Column(String(200), nullable=False)
    Product_Type = Column(String(45), nullable=False)

    def __repr__(self):
        return f"<Product(Product_ID={self.Product_ID}, Name={self.Name}, Product_Type={self.Product_Type}"

    def to_dict(self):
        return {
            "Product_ID": self.Product_ID,
            "Name": self.Name,
            "Product_Type": self.Product_Type,
        }

