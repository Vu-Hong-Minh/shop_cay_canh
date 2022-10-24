import os
from datetime import datetime
from fileinput import filename

from flask import Flask, session
from flask import request, render_template, redirect, flash, url_for
from flask_uploads import UploadSet, configure_uploads, IMAGES
from werkzeug.utils import secure_filename
from wtforms import Form, StringField, PasswordField, validators, EmailField, SelectField
from database.model import conn_SQL
from controller.handle_Product import get_list_sp_new, get_list_sp_ban_chay, get_list_sp_dm
from controller.handle_Customer import check_user_customer, check_user_employee

# Khởi tạo Flask Server Backend
app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['UPLOAD_FOLDER'] = 'static/image/product'

@app.route('/', methods=['GET'] )
def index():
    list_sp_moi = get_list_sp_new()
    list_sp_ban_chay = get_list_sp_ban_chay()
    list_sp_dm1 = get_list_sp_dm(1)
    list_sp_dm2 = get_list_sp_dm(2)
    return render_template('home.html', list_sp_moi = list_sp_moi, list_sp_ban_chay = list_sp_ban_chay, list_sp_dm1 = list_sp_dm1, list_sp_dm2 = list_sp_dm2)

class LoginForm(Form):  # Create Login Form
    username = StringField('', [validators.length(min=1)],
                           render_kw={'autofocus': True, 'placeholder': 'Username'})
    password = PasswordField('', [validators.length(min=3)],
                             render_kw={'placeholder': 'Password'})

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        # GEt user form
        username = form.username.data
        # password_candidate = request.form['password']
        password_candidate = form.password.data

        #kết nối đến mysql
        conn = conn_SQL()
        mydb = conn.connection_db()
        cur = mydb.cursor()
        result = check_user_customer(username)

        #kết quả trả về là kiểu tuple
        if result != None:
            # data = cur.fetchone()
            uid = result[0]
            name = result[2]
            if password_candidate == result[6]:
                session['logged_in'] = True
                session['uid'] = uid
                session['full_name'] = name
                x = 1
                sql1 = 'UPDATE customer SET online={} WHERE id={}'.format(x, uid)
                cur.execute(sql1)
                mydb.commit()
                # Đóng kết nối (Close connection).
                cur.close()
                mydb.close()
                return redirect(url_for('index'))

            else:
                flash('Sai mật khẩu!', 'danger')
                return render_template('login.html', form=form)
        else:
            flash('Tài khoản không tồn tại!', 'danger')
            cur.close()
            mydb.close()
            return render_template('login.html', form=form)

    return render_template('login.html', form=form)

@app.route('/out')
def logout():
    if 'uid' in session:
        # kết nối đến mysql
        conn = conn_SQL()
        mydb = conn.connection_db()
        cur = mydb.cursor()
        uid = session['uid']
        x = 0
        sql = "UPDATE customer SET online={} WHERE id={}".format(x, uid)
        cur.execute(sql)
        mydb.commit()
        session.clear()
        # Đóng kết nối (Close connection).
        cur.close()
        mydb.close()
        flash('Bạn đã đăng xuất!', 'success')
        return redirect(url_for('index'))

    return redirect(url_for('login'))

class RegisterForm(Form):
    name = StringField('', [validators.length(min=3, max=50)],
                       render_kw={'autofocus': True, 'placeholder': 'Họ tên'})
    email = EmailField('', [validators.DataRequired(), validators.Email(), validators.length(min=4, max=25)],
                       render_kw={'placeholder': 'Email'})
    password = PasswordField('', [validators.length(min=3)],
                             render_kw={'placeholder': 'Password'})
    mobile = StringField('', [validators.length(min=11, max=15)], render_kw={'placeholder': 'Mobile'})
    address = StringField('', [validators.length(min=11, max=50)], render_kw={'placeholder': 'Địa chỉ'})

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        mobile = form.mobile.data
        address = form.address.data
        now_time = datetime.now()

        conn = conn_SQL()
        mydb = conn.connection_db()
        cursor = mydb.cursor()
        result = check_user_customer(email)

        if result != None:
            flash('Email này đã tồn tại', 'info')
            return render_template('register.html', form=form)
        else:
            sql = "insert into customer (role_id, full_name, email, phone, address, pass, created_at, online) VALUES ({}, \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', {})".format(
               '1', name, email, mobile, address, password, now_time, '0')
            cursor.execute(sql)
            mydb.commit()
            # Đóng kết nối (Close connection).
            cursor.close()
            mydb.close()
        flash('Tạo tài khoản thành công!', 'success')

        return redirect(url_for('index'))

    return render_template('register.html', form=form)

@app.route('/admin')
def admin():
    # kết nối đến mysql
    conn = conn_SQL()
    mydb = conn.connection_db()
    cur = mydb.cursor()
    cur.execute("SELECT * FROM product where status_of = 1 or status_of = 2")
    result = cur.fetchall()
    cur = mydb.cursor()
    cur.execute("SELECT * FROM orders")
    read_order_row = cur.fetchall()
    cur = mydb.cursor()
    cur.execute("SELECT * FROM employee")
    read_employee_row = cur.fetchall()
    cur = mydb.cursor()


    return render_template('pages/index.html', result=result, len_result=len(result), order_rows=len(read_order_row),
                           users_rows=len(read_employee_row))


@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        # GEt user form
        username = request.form['phone']
        password_candidate = request.form['password']
        # kết nối đến mysql
        conn = conn_SQL()
        mydb = conn.connection_db()
        cur = mydb.cursor()
        result = check_user_employee(username)

        # kết quả trả về là kiểu tuple
        if result != None:
            # data = cur.fetchone()
            uid = result[0]
            name = result[2]
            if password_candidate == result[8]:
                session['logged_in'] = True
                session['uid'] = uid
                session['full_name'] = name

                return redirect(url_for('admin'))
            else:
                flash('Sai mật khẩu!', 'danger')
                return render_template('pages/login.html')

        else:
            flash('Bạn không có quyền đăng nhập hoặc tài khoản không tồn tại!', 'danger')
            # Close connection
            cur.close()
            mydb.close()
            return render_template('pages/login.html')
    return render_template('pages/login.html')

@app.route('/admin_out')
def admin_logout():
    if session['full_name'] != None:
        session.clear()
        return redirect(url_for('admin_login'))
    return redirect(url_for('admin'))

@app.route('/orders')
def orders():
    # kết nối đến mysql
    conn = conn_SQL()
    mydb = conn.connection_db()
    cur = mydb.cursor()
    cur.execute("SELECT * FROM product")
    num_rows = cur.fetchall()
    cur = mydb.cursor()
    cur.execute("SELECT * FROM orders")
    order_rows = cur.fetchall()
    cur = mydb.cursor()
    cur.execute("SELECT * FROM employee")
    result = cur.fetchall()
    cur.close()
    mydb.close()
    return render_template('pages/all_orders.html', result=order_rows, row=len(num_rows), order_rows=len(order_rows),
                           users_rows=len(result))

@app.route('/users')
def users():
    # kết nối đến mysql
    conn = conn_SQL()
    mydb = conn.connection_db()
    cur = mydb.cursor()
    cur.execute("SELECT * FROM product")
    num_rows = cur.fetchall()
    cur = mydb.cursor()
    cur.execute("SELECT * FROM orders")
    order_rows = cur.fetchall()
    cur = mydb.cursor()
    cur.execute("SELECT * FROM employee")
    result = cur.fetchall()
    cur.close()
    mydb.close()
    return render_template('pages/all_users.html', result=result, row=len(num_rows), order_rows=len(order_rows),
                           users_rows=len(result))

@app.route('/edit_product', methods=['POST', 'GET'])
def edit_product():
    if 'id' in request.args:
        #lấy id trên đường dẫn url
        product_id = request.args['id']
        # kết nối đến mysql
        conn = conn_SQL()
        mydb = conn.connection_db()
        cur = mydb.cursor()
        sql = "Select * from product where id = {}".format(product_id)
        cur.execute(sql)
        result = cur.fetchall()
        if result != None:
            if request.method == 'POST':
                category = request.form['category']
                name_plant = request.form['name_plant']
                science_name = request.form['science_name']
                price = request.form['price']
                size = request.form['size']
                image = request.files['image']
                uses = request.form['uses']
                description = request.form['description']
                care_plant = request.form['care_plant']
                status = request.form['status']
                now_time = datetime.now()
                if status == 'Không còn bán':
                    status_of = 0
                elif status == 'Đang hết hàng':
                    status_of = 1
                elif status == 'Đang bán':
                    status_of = 2
                if category and name_plant and science_name and price and size and image and uses and description and care_plant and status:
                    pic = image.filename
                    photo = pic.replace("'", "")
                    picture = photo.replace(" ", "")

                    if picture.lower().endswith(('.png', '.jpg', '.jpeg')):
                        filename = secure_filename(image.filename)
                        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                        #Tạo con trỏ
                        cur = mydb.cursor()
                        sql1 = "select id from category where name_of = \'{}\'".format(category)
                        cur.execute(sql1)
                        #Kết quả trả về là kiểu tuple
                        category_id = cur.fetchone()
                        # Tạo con trỏ
                        cur = mydb.cursor()
                        sql2 = "update product set category_id = {}, name_of = \'{}\', science_name = \'{}\', price = {}, size = \'{}\', image = \'{}\', uses = \'{}\', description = \'{}\', care_plant = \'{}\', updated_at = \'{}\', updated_by = {}, status_of = {} where id = {}".format(
                                category_id[0], name_plant, science_name, price, size, picture, uses, description, care_plant, now_time, session['uid'], status_of, product_id
                        )
                        cur.execute(sql2)
                        mydb.commit()
                        #Tạo con trỏ
                        cur = mydb.cursor()
                        sql3 = "select image from product where id = {}".format(product_id)
                        cur.execute(sql3)
                        # Kết quả trả về là kiểu tuple
                        product_image = cur.fetchone()
                        if product_image[0] == picture:
                            flash('Updated thành công!', 'success')
                            return redirect(url_for('admin'))
                        else:
                            flash('Updated thất bại!', 'danger')
                            return redirect(url_for('edit_product'))
                    else:
                        flash('Định dạng file không hỗ trợ!', 'danger')
                        return render_template('pages/edit_product.html', result=result)
                else:
                    flash('Bạn phải điền đủ thông tin!', 'danger')
                    return render_template('pages/edit_product.html', result=result)
            else:
                return render_template('pages/edit_product.html', result=result)
        else:
            return redirect(url_for('admin_login'))
    else:
        return redirect(url_for('admin_login'))

@app.route('/delete_product', methods=['POST', 'GET'])
def delete_product():
    if 'id' in request.args:
        # lấy id trên đường dẫn url
        product_id = request.args['id']
        if session['full_name'] != None:
            # kết nối đến mysql
            conn = conn_SQL()
            mydb = conn.connection_db()
            cur = mydb.cursor()
            sql = "update product set status_of = 0 where id = {}".format(product_id)
            cur.execute(sql)
            mydb.commit()
            # Đóng kết nối
            cur.close()
            mydb.close()

            flash("Xóa sản phẩm thành công!", "success")
            return redirect(url_for('admin'))

        else:
            return redirect(url_for('admin_login'))


@app.route('/admin_add_product', methods=['POST', 'GET'])
def admin_add_product():
    if session['full_name'] != None:
        if request.method == 'POST':
            category_name = request.form['category_id']
            name_of = request.form['name_of']
            science_name = request.form['science_name']
            price = request.form['price']
            size = request.form['product_size']
            image = request.files['image']
            uses = request.form['uses']
            description = request.form['description']
            care_plant = request.form['care_plant']
            quantity = int(request.form['quantity'])
            if category_name == 'Cây dây leo':
                category_id = 1
            elif category_name == 'Cây công trình':
                category_id = 2
            elif category_name == 'Cây giống':
                category_id = 3
            elif category_name == 'Cây thủy sinh':
                category_id = 4
            elif category_name == 'Cây không khí':
                category_id = 6
            elif category_name == 'Cây để bàn':
                category_id = 7
            elif category_name == 'Bonsai cây cảnh':
                category_id = 8
            elif category_name == 'Cây bám tường':
                category_id = 9
            elif category_name == 'Cây ăn quả':
                category_id = 10
            elif category_name == 'Cây trồng trong nước':
                category_id = 11
            elif category_name == 'Cây may mắn':
                category_id = 12
            elif category_name == 'Cây nội thất':
                category_id = 13

            pic = image.filename
            photo = pic.replace("'", "")
            picture = photo.replace(" ", "")
            now_time = datetime.now()

            if category_name and name_of and science_name and price and size and image and uses and description and care_plant:
                # kết nối đến mysql
                conn = conn_SQL()
                mydb = conn.connection_db()
                cur = mydb.cursor()
                sql = "Insert into product (category_id, name_of, science_name, price, size, image, uses, description, care_plant, created_at, status_of, quantity) values ({}, \'{}\', \'{}\', {}, \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', {}, {})".format(
                    category_id, name_of, science_name, price, size, picture, uses, description, care_plant, now_time, 2, quantity
                )
                cur.execute(sql)
                mydb.commit()
                #Đóng kết nối
                cur.close()
                mydb.close()

                if picture.lower().endswith(('.png', '.jpg', '.jpeg')):
                    filename = secure_filename(image.filename)
                    image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    flash('Thêm sản phẩm thành công!', 'success')
                    return redirect(url_for('admin'))

                else:
                    flash('File định dạng không hợp lệ!', 'danger')
                    return render_template('pages/add_product.html')

            else:
                flash('Bạn phải điền đủ thông tin!', 'danger')
                return render_template('pages/add_product.html')

        else:
            return render_template('pages/add_product.html')
    else:
        return redirect(url_for('admin_login'))

@app.route('/product_trash', methods=['POST', 'GET'])
def product_trash():
    # kết nối đến mysql
    conn = conn_SQL()
    mydb = conn.connection_db()
    cur = mydb.cursor()
    cur.execute("SELECT * FROM product where status_of = 0")
    result = cur.fetchall()

    return render_template('pages/product_trash.html', result=result)


@app.route('/restore_product', methods=['POST', 'GET'])
def restore_product():
    if session['full_name'] != None:
        if 'id' in request.args:
            # lấy id trên đường dẫn url
            product_id = request.args['id']
            if session['logged_in'] == True:
                # kết nối đến mysql
                conn = conn_SQL()
                mydb = conn.connection_db()
                cur = mydb.cursor()
                sql = "update product set status_of = 2 where id = {}".format(product_id)
                cur.execute(sql)
                mydb.commit()
                # Đóng kết nối
                cur.close()
                mydb.close()

                flash("Khôi phục sản phẩm thành công!", "success")
                return redirect(url_for('admin'))

            else:
                return redirect(url_for('admin_login'))
        else:
            flash("Khôi phục sản phẩm thất bại!", "danger")
            return redirect(url_for('restore_product'))
    else:
        return redirect(url_for('admin_login'))

@app.route('/admin_add_employee', methods=['POST', 'GET'])
def admin_add_employee():
    if session['full_name'] != None:
        if request.method == 'POST':
            full_name = request.form['full_name']
            phone = request.form['phone']
            date_of_birth = request.form['date_of_birth']
            gender = request.form['gender']
            address = request.form['address']
            job_position = request.form['job_position']
            password = request.form['password']
            now_time = datetime.now()

            if full_name and phone and date_of_birth and gender and address and job_position and password:
                # kết nối đến mysql
                conn = conn_SQL()
                mydb = conn.connection_db()
                cur = mydb.cursor()
                sql = "Insert into employee (role_id, full_name, phone, date_of_birth, gender, address, job_position, password, created_at, status_of) values ({}, \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', {})".format(
                        1, full_name, phone, date_of_birth, gender, address, job_position, password, now_time, 1
                )
                cur.execute(sql)
                mydb.commit()
                # Đóng kết nối
                cur.close()
                mydb.close()
                flash('Thêm nhân viên thành công!', 'success')
                return redirect(url_for('admin'))
            else:
                flash('Bạn phải điền đủ thông tin!', 'danger')
                return render_template('pages/add_employee.html')
        else:
            return render_template('pages/add_employee.html')
    else:
        return redirect(url_for('admin_login'))

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port='6868')
