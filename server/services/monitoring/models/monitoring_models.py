from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import LONGTEXT
from server.database.mysqlDB import Base


class AlarmsTemplatesModels(Base):
    __tablename__ = "monitoring_templates_alarms"

    id = Column(String(512), primary_key=True)
    name = Column(String(64), nullable=False)
    domain = Column(String(448), nullable=False)
    template = Column(LONGTEXT(), nullable=False)
    variables = Column(LONGTEXT(), nullable=False)


    def __repr__(self):
        return f"<AlarmsTemplatesModels(name={self.name}, domain={self.domain}, template={self.template})>"

    def to_dict(self):
        return {
            "name": self.name,
            "domain": self.domain,
            "template": self.template,
            "variables": self.variables
        }

