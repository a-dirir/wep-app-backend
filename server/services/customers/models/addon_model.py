from sqlalchemy import Column, String
from server.database.mysqlDB import Base


class AddonModel(Base):
    __tablename__ = "addons"
    Addon_ID = Column(String(100), primary_key=True)
    Name = Column(String(200), nullable=False)
    Addon_Type = Column(String(45), nullable=False)

    def __repr__(self):
        return f"<Addon(Addon_ID={self.Addon_ID}, Name={self.Name}, Addon_Type={self.Addon_Type}"

    def to_dict(self):
        return {
            "Addon_ID": self.Addon_ID,
            "Name": self.Name,
            "Addon_Type": self.Addon_Type,
        }

