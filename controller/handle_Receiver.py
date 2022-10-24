from database.model import conn_SQL

def get_info_receiver(receiver_id):
    try:
        conn = conn_SQL()
        mydb = conn.connection_db()
        cursor = mydb.cursor()
        sql = "Select phone, address from Receiver where id = {}".format(receiver_id)
        cursor.execute(sql)
        row = cursor.fetchone()
        while row is not None:
            print(row)
            row = cursor.fetchone()

    finally:
        # Đóng kết nối (Close connection).
        cursor.close()
        mydb.close()