import os
from sqlalchemy import create_engine, URL
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class MySQLDB:
    def __init__(self):
        self.url = URL.create(
            "mysql+mysqlconnector",
            username=os.getenv("MySQL_User"),
            password=os.getenv("MySQL_Password"),
            host=f"{os.getenv('MySQL_IP')}",
            database=os.getenv("MySQL_Name"),
        )

        self.engine = create_engine(self.url, echo=False)

    def create_tables(self):
        Base.metadata.create_all(self.engine)

