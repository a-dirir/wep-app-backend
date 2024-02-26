from sqlalchemy import Column, String, DateTime
from server.database.mysqlDB import Base


class SyntheticModel(Base):
    __tablename__ = "clients_url"
    Sub_Client_ID = Column(String(80))
    URL = Column(String(100), nullable=False, primary_key=True)
    URL_SSL_Expiry_Date = Column(String(50))

    def __repr__(self):
        return f"<Synthetic(Sub_Client_ID={self.Sub_Client_ID}, URL={self.URL}, URL_SSL_Expiry_Date={self.URL_SSL_Expiry_Date}"

    def to_dict(self):
        return {
            "Sub_Client_ID": self.Sub_Client_ID,
            "URL": self.URL,
            "URL_SSL_Expiry_Date": self.URL_SSL_Expiry_Date
        }