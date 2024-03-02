import mysql.connector
from server.database.schema import schema


class MySQLDB:
    def __init__(self, host: str, user: str, password: str, database: str):
        self.mydb = mysql.connector.connect(host=host, user=user, password=password, database=database)

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
    def convert_results_to_dict(table_name: str, rows: list):
        columns = schema[table_name]['columns']
        result = []
        for row in rows:
            row_dict = {}
            for i in range(len(columns)):
                row_dict[list(columns.keys())[i]] = row[i]
            result.append(row_dict)

        return result

    def get_rows(self, table_name: str, columns: list = None, where_items: list = None, distinct: str = ""):
        try:
            if columns is None:
                columns = ['*']
            columns = ", ".join(columns)
            sql = f"SELECT {distinct} {columns} FROM {table_name}"
            if where_items is not None:
                where_clause = self.generate_where_clause(where_items)
                sql = f"{sql} WHERE {where_clause}"
            mycursor = self.mydb.cursor()
            mycursor.execute(sql)
            results = self.convert_results_to_dict(table_name, mycursor.fetchall())

            return True, results
        except Exception as e:
            return False, f"Error fetching rows from Table ({table_name})\n{e}"

    def insert_row(self, table_name: str, row: dict):
        try:
            keys = ", ".join(row.keys())
            values = tuple(row.values())
            sql = f"INSERT INTO {table_name} ({keys}) VALUES {values}"
            mycursor = self.mydb.cursor()
            mycursor.execute(sql)
            self.mydb.commit()
            return True, f"Row inserted successfully"
        except Exception as e:
            return False, f"Error fetching rows from Table ({table_name})\n{e}"

    def update_row(self, table_name: str, row: dict, where_items: list):
        try:
            set_clause = ""
            for key, value in row.items():
                if value[0] != "'" and value[-1] != "'":
                    value = f"'{value}'"

                set_clause = f"{set_clause}{key} = {value}, "
            set_clause = set_clause[:-2]

            where_clause = self.generate_where_clause(where_items)
            sql = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause};"
            mycursor = self.mydb.cursor()
            mycursor.execute(sql)
            self.mydb.commit()
            return True, f"Row updated successfully"
        except Exception as e:
            return False, f"Error updating rows in Table ({table_name})\n{e}"

    def delete_row(self, table_name: str, where_items: list):
        try:
            where_clause = self.generate_where_clause(where_items)
            sql = f"DELETE FROM {table_name} WHERE {where_clause}"
            mycursor = self.mydb.cursor()
            mycursor.execute(sql)
            self.mydb.commit()
            return True, f"Row deleted successfully"
        except Exception as e:
            return False, f"Error deleting rows in Table ({table_name})\n{e}"

    def close(self):
        self.mydb.close()
        return True, "Connection closed successfully"

