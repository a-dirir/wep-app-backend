from sqlalchemy import Column, String, Integer
from server.database.mysqlDB import Base


class ContactModel(Base):
    __tablename__ = "clients_contacts"
    Contact_ID = Column(Integer, nullable=False, primary_key=True)
    Sub_Client_ID = Column(String(80), nullable=False)
    Account_Manager = Column(String(80))
    MS_Focal_Point = Column(String(80))
    Domain = Column(String(100))
    Contact_Type = Column(String(80))
    Position = Column(String(80))
    Contact_Name = Column(String(120))
    Contact_Email = Column(String(80))
    Contact_Number = Column(String(45))

    def __repr__(self):
        return f"<Contact(Name={self.Contact_Name}, Contact_Type={self.Contact_Type}"

    def to_dict(self):
        return {
            "Contact_ID": self.Contact_ID,
            "Sub_Client_ID": self.Sub_Client_ID,
            "Account_Manager": self.Account_Manager,
            "MS_Focal_Point": self.MS_Focal_Point,
            "Domain": self.Domain,
            "Contact_Type": self.Contact_Type,
            "Position": self.Position,
            "Contact_Name": self.Contact_Name,
            "Contact_Email": self.Contact_Email,
            "Contact_Number": self.Contact_Number
        }