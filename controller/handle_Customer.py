from database.model import conn_SQL

def check_user_customer(email):
    try:
        conn = conn_SQL()
        mydb = conn.connection_db()
        cursor = mydb.cursor()
        sql = 'Select * from Shop_Cay_Canh.customer where email = \'{}\''.format(email)
        cursor.execute(sql)
        result = cursor.fetchone()
    finally:
        # Đóng kết nối (Close connection).
        cursor.close()
        mydb.close()

    return result

def check_user_employee(phone):
    try:
        conn = conn_SQL()
        mydb = conn.connection_db()
        cursor = mydb.cursor()
        sql = 'Select * from Shop_Cay_Canh.employee where phone = \'{}\' and (job_position = \'Nhân viên chốt đơn\' or job_position = \'Quản lý cửa hàng\')'.format(phone)
        cursor.execute(sql)
        result = cursor.fetchone()
    finally:
        # Đóng kết nối (Close connection).
        cursor.close()
        mydb.close()

    return result
