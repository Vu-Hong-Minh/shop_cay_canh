from database.model import conn_SQL

def get_info_cart(customer_id):
    try:
        conn = conn_SQL()
        mydb = conn.connection_db()
        cursor = mydb.cursor()
        sql = "select Product.name_of, Cart.quantity, Product.price, Product.price * Cart.quantity as 'Thành tiền' from Product inner join Cart ON Product.id = Cart.product_id where Cart.customer_id = {}".format(customer_id)
        cursor.execute(sql)
        row = cursor.fetchone()
        while row is not None:
            print(row)
            row = cursor.fetchone()

    finally:
        # Đóng kết nối (Close connection).
        cursor.close()
        mydb.close()

def total_money_order(customer_id):
    try:
        conn = conn_SQL()
        mydb = conn.connection_db()
        cursor = mydb.cursor()
        sql = "Select Sum(Table1.Thanhtien) as Tongtien from (select Product.name_of, Product.price * Cart.quantity as Thanhtien from Product inner join Cart ON Product.id = Cart.product_id where Cart.customer_id = {}) as Table1".format(customer_id)
        cursor.execute(sql)
        row = cursor.fetchone()
        total_money = row[0]

    finally:
        # Đóng kết nối (Close connection).
        cursor.close()
        mydb.close()

    return total_money