import mysql.connector
# Kết nối vào database.
class conn_SQL:
    def __init__(self, host = 'localhost', db = 'shop_cay_canh', user = 'root', password = '123456@Aabc'):
        self.host = host
        self.db = db
        self.user = user
        self.password = password

    def connection_db(self):
        mydb = mysql.connector.connect(host=self.host, database=self.db, user=self.user, password=self.password)
        return mydb