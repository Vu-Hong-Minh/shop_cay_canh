from database.model import conn_SQL

def info_Category_name(category_id):
    #Hàm lấy danh sách sản phẩm theo tên danh mục
    try:
        conn = conn_SQL()
        mydb = conn.connection_db()
        cursor = mydb.cursor()
        sql = "SELECT Table1.name_of, Product.name_of from (select Relationship_P_C.category_id,Category.name_of, Relationship_P_C.product_id from Category inner join Relationship_P_C On Relationship_P_C.category_id = {} and Category.id = Relationship_P_C.category_id) as Table1 inner join Product On Table1.product_id = Product.id;".format(category_id)
        cursor.execute(sql)
        row = cursor.fetchone()
        while row is not None:
            print(row)
            row = cursor.fetchone()

    finally:
        # Đóng kết nối (Close connection).
        cursor.close()
        mydb.close()

def info_product_sort(table, col, request):
    #Sắp xếp danh sách sản phẩm theo tên/giá theo chiều tăng/giảm
    try:
        conn = conn_SQL()
        mydb = conn.connection_db()
        cursor = mydb.cursor()
        sql = "Select * from {} Order by {} {}".format(table, col, request)
        cursor.execute(sql)
        row = cursor.fetchone()
        while row is not None:
            print(row)
            row = cursor.fetchone()

    finally:
        # Đóng kết nối (Close connection).
        cursor.close()
        mydb.close()

def info_product_price(price_from, price_to):
    #Lọc danh sách sản phẩm theo khoảng giá
    try:
        conn = conn_SQL()
        mydb = conn.connection_db()
        cursor = mydb.cursor()
        sql = "Select * from Product where {} < price and price < {}".format(price_from, price_to)
        cursor.execute(sql)
        row = cursor.fetchone()
        while row is not None:
            print(row)
            row = cursor.fetchone()

    finally:
        # Đóng kết nối (Close connection).
        cursor.close()
        mydb.close()

def check_quantity():
    pass

def get_info_product(product_id):
    #Lấy thông tin chi tiết sản phẩm
    try:
        conn = conn_SQL()
        mydb = conn.connection_db()
        cursor = mydb.cursor()
        sql = "Select * from Product where id = {}".format(product_id)
        cursor.execute(sql)
        row = cursor.fetchone()
        while row is not None:
            print(row)
            row = cursor.fetchone()

    finally:
        # Đóng kết nối (Close connection).
        cursor.close()
        mydb.close()

def get_list_sp_new():
    try:
        conn = conn_SQL()
        mydb = conn.connection_db()
        cursor = mydb.cursor()
        sql = "SELECT product.id, product.name_of, product.price, product.image FROM shop_cay_canh.product where date(now()) - created_at < 30 LIMIT 4"
        cursor.execute(sql)
        list_sp_moi = cursor.fetchall()
        return list_sp_moi
    finally:
        # Đóng kết nối (Close connection).
        cursor.close()
        mydb.close()


def get_list_sp_ban_chay():
    try:
        conn = conn_SQL()
        mydb = conn.connection_db()
        cursor = mydb.cursor()
        sql = "select product.id, product.name_of, product.price, product.image from product inner join (select product_id, sum(quantity * price) as 'Tongtien' from order_detail group by product_id order by Tongtien DESC) as Table1 on product.id = Table1.product_id limit 4"
        cursor.execute(sql)
        list_sp_moi = cursor.fetchall()
        return list_sp_moi
    finally:
        # Đóng kết nối (Close connection).
        cursor.close()
        mydb.close()

def get_list_sp_dm(id):
    try:
        conn = conn_SQL()
        mydb = conn.connection_db()
        cursor = mydb.cursor()
        sql = " select product.id, product.name_of, product.price, product.image from product where category_id = {} limit 4".format(id)
        cursor.execute(sql)
        list_sp_moi = cursor.fetchall()
        return list_sp_moi
    finally:
        # Đóng kết nối (Close connection).
        cursor.close()
        mydb.close()
