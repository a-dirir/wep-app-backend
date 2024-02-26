from sqlalchemy import Column, String
from server.database.mysqlDB import Base


class AwsAccountModel(Base):
    __tablename__ = "aws_accounts"
    Account_ID = Column(String(100), nullable=False, primary_key=True)
    Sub_Client_ID = Column(String(100))
    Name = Column(String(200))
    Master_Account = Column(String(100))
    region = Column(String(50))

    def __repr__(self):
        return f"<AWSAccount(Account_ID={self.Account_ID}, Sub_Client_ID={self.Sub_Client_ID}, Name={self.Name}, Master_Account={self.Master_Account}, region={self.region})"

    def to_dict(self):
        return {
            "Account_ID": self.Account_ID,
            "Sub_Client_ID": self.Sub_Client_ID,
            "Name": self.Name,
            "Master_Account": self.Master_Account,
            "region": self.region
        }