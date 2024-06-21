from dotenv import load_dotenv
from server.api.server import Server
from server.database.mysql_db import MySQLDB
from os import getenv


def load_db():

    return MySQLDB(
        host=getenv("MYSQL_Endpoint"),
        user=getenv("MYSQL_User"),
        password=getenv("MYSQL_Password"),
        database=getenv("MYSQL_Name")
    )


if __name__ == '__main__':
    load_dotenv("config.env")

    db = load_db()
    website_dir = getenv("WEB_DIR")

    server = Server(db, website_dir)


