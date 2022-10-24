from database.model import conn_SQL

def insert_order():
    pass

def get_thumbnails(product_id):
    try:
        conn = conn_SQL()
        mydb = conn.connection_db()
        cursor = mydb.cursor()
        sql = "Select * from Gallery where product_id = {}".format(product_id)
        cursor.execute(sql)
        row = cursor.fetchone()
        while row is not None:
            print(row)
            row = cursor.fetchone()

    finally:
        # Đóng kết nối (Close connection).
        cursor.close()
        mydb.close()

def get_all_info_order(customer_id):
    # Lấy ra tất cả đơn hàng của một khách hàng
    try:
        conn = conn_SQL()
        mydb = conn.connection_db()
        cursor = mydb.cursor()
        sql = "Select * from Orders where customer_id = {}".format(customer_id)
        cursor.execute(sql)
        row = cursor.fetchone()
        while row is not None:
            print(row)
            row = cursor.fetchone()

    finally:
        # Đóng kết nối (Close connection).
        cursor.close()
        mydb.close()



def get_info_order(customer_id, status_of):
    # Lấy ra đơn hàng theo trạng thái đơn hàng của một khách hàng
    try:
        conn = conn_SQL()
        mydb = conn.connection_db()
        cursor = mydb.cursor()
        sql = "Select * from Orders where customer_id = {} and status_of = {}".format(customer_id, status_of)
        cursor.execute(sql)
        row = cursor.fetchone()
        while row is not None:
            print(row)
            row = cursor.fetchone()

    finally:
        # Đóng kết nối (Close connection).
        cursor.close()
        mydb.close()


def get_list_receiver(customer_id):
    try:
        conn = conn_SQL()
        mydb = conn.connection_db()
        cursor = mydb.cursor()
        sql = "Select Receiver.full_name, Table3.Total_receipt from Receiver inner join (Select Table1.full_name as NguoiDat, Table1.receiver_id, Table2.Total_receipt from (Select Customer.full_name, Relationship_C_R.receiver_id from Customer inner join Relationship_C_R On Customer.id = {} where Relationship_C_R.customer_id = Customer.id) as Table1 inner join (select receiver_id, count(Orders.receiver_id) as 'Total_receipt' from Orders group by receiver_id) as Table2 On Table1.receiver_id = Table2.receiver_id) as Table3 On Table3.receiver_id = Receiver.id".format(customer_id)
        cursor.execute(sql)
        row = cursor.fetchone()
        while row is not None:
            print(row)
            row = cursor.fetchone()

    finally:
        # Đóng kết nối (Close connection).
        cursor.close()
        mydb.close()