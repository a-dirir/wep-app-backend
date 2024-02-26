from sqlalchemy import Column, String, TEXT
from server.database.mysqlDB import Base


class AzureAccountModel(Base):
    __tablename__ = "azure_accounts"
    Subscription_ID = Column(String(100), nullable=False, primary_key=True)
    Sub_Client_ID = Column(String(100))
    Name = Column(TEXT(), nullable=False)
    Tenant_ID = Column(String(100))

    def __repr__(self):
        return f"<AWSAccountModel(Subscription_ID={self.Subscription_ID}, Sub_Client_ID={self.Sub_Client_ID}, Name={self.Name}, Tenant_ID={self.Tenant_ID})"

    def to_dict(self):
        return {
            "Subscription_ID": self.Subscription_ID,
            "Sub_Client_ID": self.Sub_Client_ID,
            "Name": self.Name,
            "Tenant_ID": self.Tenant_ID
        }