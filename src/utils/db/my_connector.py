import mysql.connector
from mysql.connector import errorcode

config = {
    'user': 'root',
    'password': 'root',
    'host': '127.0.0.1',
    'port': '3307',
    #   'database': 'employees',
    'raise_on_warnings': True
}


class MYConnector:

    def __init__(self, config):
        self.config = config
        self.cnx = None
        self.cursor = None

    def connect(self):
        try:
            self.cnx = mysql.connector.connect(**self.config)
            self.cursor = self.cnx.cursor()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
            return None
        return self.cnx

    def close(self):
        self.cursor.close()
        self.cnx.close()

    def commit(self):
        self.cursor.commit()

    def query(self, query_text):
        self.cursor.execute(query_text)
        return self.cursor.fetchall()
