from sqlalchemy import Column, String, TEXT
from server.database.mysqlDB import Base


class M365AccountModel(Base):
    __tablename__ = "m365_accounts"
    Tenant_ID = Column(String(100), nullable=False, primary_key=True)
    Sub_Client_ID = Column(String(100))
    Name = Column(String(200), nullable=False)

    def __repr__(self):
        return f"<AWSAccountModel(Sub_Client_ID={self.Sub_Client_ID}, Name={self.Name}, Tenant_ID={self.Tenant_ID})"

    def to_dict(self):
        return {
            "Sub_Client_ID": self.Sub_Client_ID,
            "Name": self.Name,
            "Tenant_ID": self.Tenant_ID
        }
