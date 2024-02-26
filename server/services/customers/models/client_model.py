from sqlalchemy import Column, String
from server.database.mysqlDB import Base


class ClientModel(Base):
    __tablename__ = "clients"
    Client_ID = Column(String(100), nullable=False, primary_key=True)
    Name = Column(String(200))

    def __repr__(self):
        return f"<Client(Client_ID={self.Client_ID}, Name={self.Name})"

    def to_dict(self):
        return {
            "Client_ID": self.Client_ID,
            "Name": self.Name
        }