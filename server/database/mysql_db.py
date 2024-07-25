import mysql.connector
import mysql.connector.pooling
from server.database.schema import schema
from server.util import get_logger
from os import environ


class MySQLDB:
    def __init__(self):
        self.pool = mysql.connector.pooling.MySQLConnectionPool(
            pool_name="crm_pool",
            pool_size=10,
            pool_reset_session=True,
            host=environ.get("MYSQL_HOST"),
            user=environ.get("MYSQL_USER"),
            password=environ.get("MYSQL_PASSWORD"),
            database=environ.get("MYSQL_DATABASE_NAME"),
            ssl_ca='crm-ca.pem'
        )
        
        self.logger = get_logger(__name__)

    def get_connection(self):
        return self.pool.get_connection()

    @staticmethod
    def generate_where_clause(where_items: list):
        # where_items is list of dictionaries, where each dictionary is a condition,
        # use AND to join them, and OR to join list items

        where_clause = ""
        for item in where_items:
            for key, value in item.items():
                # enclose value in single quotes if it is a string
                if value[0] != "'" and value[-1] != "'":
                    value = f"'{value}'"

                if where_clause == "" or where_clause[-3:] == "OR ":
                    where_clause = f"{where_clause}{key} = {value}"
                else:
                    where_clause = f"{where_clause} AND {key} = {value}"

            if where_clause != "":
                where_clause = f"{where_clause} OR "

        if where_clause != "":
            where_clause = where_clause[:-4]

        return where_clause

    @staticmethod
    def convert_results_to_dict(rows: list, columns: list = None):
        result = []
        for row in rows:
            row_dict = {}
            for i in range(len(columns)):
                row_dict[columns[i]] = str(row[i])
            result.append(row_dict)
        return result

    def get_rows(self, table_name: str, columns: list = None, where_items: list = None, distinct: str = "",
                 return_type: str = "dict"):
        cursor = None
        db = None

        try:
            db = self.get_connection()
            if columns is None:
                columns = list(schema[table_name]['columns'].keys())
            columns_str = ", ".join(columns)
            sql = f"SELECT {distinct} {columns_str} FROM {table_name}"
            if where_items is not None:
                where_clause = self.generate_where_clause(where_items)
                sql = f"{sql} WHERE {where_clause}"

            cursor = db.cursor()
            cursor.execute(sql)
            results = cursor.fetchall()

            if return_type == "dict":
                results = self.convert_results_to_dict(results, columns)
            
            self.logger.info(f"Rows fetched successfully {sql}")
            return True, results

        except Exception as e:
            self.logger.error(f"Error fetching rows from Table ({table_name}) {sql} \n{e}")
            return False, f"Error fetching data from database"
        finally:
            if cursor is not None:
                cursor.close()
            if db is not None:
                db.close()

    def insert_row(self, table_name: str, row: dict):
        cursor = None
        db = None

        try:
            db = self.get_connection()
            keys = ", ".join(row.keys())
            values = tuple(row.values())
            sql = f"INSERT INTO {table_name} ({keys}) VALUES {values}"
            cursor = db.cursor()
            cursor.execute(sql)
            db.commit()
            self.logger.info(f"Row inserted successfully {sql}")
            return True, f"Row inserted successfully"
        except Exception as e:
            self.logger.error(f"Error inserting rows into Table ({table_name}) {sql} \n{e}")
            return False, f"Error inserting rows into database"
        finally:
            if cursor is not None:
                cursor.close()
            if db is not None:
                db.close()

    def update_row(self, table_name: str, row: dict, where_items: list):
        cursor = None
        db = None

        try:
            db = self.get_connection()
            set_clause = ""
            for key, value in row.items():
                if value[0] != "'" and value[-1] != "'":
                    value = f"'{value}'"

                set_clause = f"{set_clause}{key} = {value}, "
            set_clause = set_clause[:-2]

            where_clause = self.generate_where_clause(where_items)
            sql = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause};"
            cursor = db.cursor()
            cursor.execute(sql)
            db.commit()
            self.logger.info(f"Row updated successfully {sql}")
            return True, f"Row updated successfully"
        except Exception as e:
            self.logger.error(f"Error updating rows in Table ({table_name}) {sql} \n{e}")
            return False, f"Error updating rows in Table ({table_name})\n{e}"
        finally:
            if cursor is not None:
                cursor.close()
            if db is not None:
                db.close()

    def delete_row(self, table_name: str, where_items: list):
        cursor = None
        db = None

        try:
            db = self.get_connection()
            where_clause = self.generate_where_clause(where_items)
            sql = f"DELETE FROM {table_name} WHERE {where_clause}"
            cursor = db.cursor()
            cursor.execute(sql)
            db.commit()
            self.logger.info(f"Row deleted successfully {sql}")
            return True, f"Row deleted successfully"
        except Exception as e:
            self.logger.error(f"Error deleting rows in Table ({table_name}) {sql} \n{e}")
            return False, f"Error deleting rows in Table ({table_name})\n{e}"
        finally:
            if cursor is not None:
                cursor.close()
            if db is not None:
                db.close()

    def close(self):
        try:
            db = self.get_connection()
            db.close()
            return True, "Connection closed successfully"
        except Exception as e:
            return False, f"Error closing connection\n{e}"

