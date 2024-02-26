from sqlalchemy import Column, String, DateTime
from server.database.mysqlDB import Base


class SubClientModel(Base):
    __tablename__ = "sub_clients"
    Sub_Client_ID = Column(String(100), nullable=False, primary_key=True)
    Name = Column(String(200))
    Status = Column(String(45))
    Client_ID = Column(String(100))
    First_Engagement_Date = Column(DateTime())
    Engagement_Year = Column(String(45))
    Engagement_Quarter = Column(String(45))

    def __repr__(self):
        return f"<SubClient(Sub_Client_ID={self.Sub_Client_ID}, Name={self.Name}, Status={self.Status}, Client_ID={self.Client_ID}, First_Engagement_Date={self.First_Engagement_Date}, Engagement_Year={self.Engagement_Year}, Engagement_Quarter={self.Engagement_Quarter})"

    def to_dict(self):
        return {
            "Sub_Client_ID": self.Sub_Client_ID,
            "Name": self.Name,
            "Status": self.Status,
            "Client_ID": self.Client_ID,
            "First_Engagement_Date": self.First_Engagement_Date,
            "Engagement_Year": self.Engagement_Year,
            "Engagement_Quarter": self.Engagement_Quarter
        }
