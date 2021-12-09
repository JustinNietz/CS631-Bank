from typing import List, Dict
import simplejson as json
import os
from flask import Flask, request, Response, redirect, url_for, session, flash
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
from flask_mail import Mail, Message


app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)
app.secret_key = "123456"

app.config['SECRET_KEY'] = 'top-secret!'
app.config['MAIL_SERVER'] = 'smtp.sendgrid.net'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'apikey'
app.config['MAIL_PASSWORD'] = os.environ.get('SENDGRID_API_KEY')
app.config['MAIL_DEFAULT_SENDER'] = 'nietzersche@gmail.com'
mail = Mail(app)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'bankData'

mysql.init_app(app)

db = MySQL(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['GET', 'POST'])
def account_success():
    return render_template('accountsuccess.html')

@app.route('/about')
def about_page():
    return render_template('about.html')

@app.route('/emplogin', methods=['GET', 'POST'])
def emp_login_check():
    if request.method == 'POST':
        if 'username' in request.form and 'password' in request.form:
            username = request.form['username']
            password = request.form['password']
            cursor = mysql.get_db().cursor()
            cursor.execute("SELECT * FROM employee WHERE EmpLogin=%s AND EmpPassword=%s", (username, password))
            info = cursor.fetchone()
            if info is not None:
                if info['EmpLogin'] == username and info['EmpPassword'] == password:
                    session['loginsuccess'] = True
                    return redirect(url_for("emp_home_page"))
            else:
                return redirect(url_for("emp_login_check"))

    return render_template("emplogin.html")

@app.route('/custlogin', methods=['GET', 'POST'])
def cust_login_check():
    if request.method == 'POST':
        if 'username' in request.form and 'password' in request.form:
            username = request.form['username']
            password = request.form['password']
            cursor = mysql.get_db().cursor()
            cursor.execute("SELECT * FROM customer WHERE CustomerLogin=%s AND CustomerPassword=%s", (username, password))
            info = cursor.fetchone()
            if info is not None:
                if info['CustomerLogin'] == username and info['CustomerPassword'] == password:
                    session['loginsuccess'] = True
                    return redirect(url_for("cust_home_page"))
            else:
                return redirect(url_for("cust_login_check"))

    return render_template("custlogin.html")

@app.route('/register', methods=['GET', 'POST'])
def new_user():
    if request.method == "POST":
        recipient = request.form['two']
        msg = Message('Thanks for signing up to CS631Bank!', recipients=[recipient])
        if "one" in request.form and "two" in request.form and "three" in request.form:
            customername = request.form['one']
            cust_ssn = request.form['two']
            city = request.form['three']
            state = request.form['four']
            zipcode = request.form['five']
            streetnum = request.form['six']
            username = request.form['seven']
            password = request.form['eight']
            cursor = mysql.get_db().cursor()
            cursor.execute('INSERT INTO customer(customer_ssn, city, state, zipcode, streetnum, customername, customerlogin, customerpassword)VALUES(%s,%s,%s,%s,%s,%s,%s,%s)', (cust_ssn, city, state, zipcode, streetnum, customername, username, password))
            mysql.get_db().commit()
            return redirect(url_for('account_success'))
    return render_template("register.html")



@app.route('/emphomepage', methods=['GET'])
def emp_home_page():
    if session['loginsuccess'] == True:
        user = {'username': 'Your'}
        cursor = mysql.get_db().cursor()
        cursor.execute('SELECT * FROM customer')
        result = cursor.fetchall()
        return render_template('empview.html', title='Customer', user=user, customers=result)

@app.route('/custhomepage', methods=['GET'])
def cust_home_page():
    if session['loginsuccess'] == True:
        user = {'username': 'Your'}
        cursor = mysql.get_db().cursor()
        cursor.execute('SELECT * FROM customer')
        result = cursor.fetchall()
        return render_template('custview.html', title='Home', user=user, homes=result)


@app.route('/logout')
def logout():
    session.pop('loginsuccess',None)
    return redirect(url_for('index'))

@app.route('/view/<int:customer_id>', methods=['GET'])
def record_view(customer_id):
    values = []
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM customer WHERE Customer_SSN=%s', customer_id)
    result = cursor.fetchall()
    return render_template('view.html', title='Customer', max=300, customer=result[0], values=values)

@app.route('/edit/<int:customer_id>', methods=['GET'])
def form_edit_get(customer_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM customer WHERE Customer_SSN=%s', customer_id)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', customer=result[0])


@app.route('/edit/<int:customer_id>', methods=['POST'])
def form_update_post(customer_id):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('City'), request.form.get('State'),
                 request.form.get('ZipCode'), request.form.get('StreetNum'),
                 request.form.get('CustomerName'), request.form.get('CustomerLogin'), request.form.get('CustomerPassword'),
                 customer_id)
    sql_update_query = """UPDATE customer t SET t.City = %s, t.State = %s, t.ZipCode = 
    %s, t.StreetNum = %s, t.CustomerName = %s, t.CustomerLogin = %s, t.CustomerPassword = %s WHERE t.Customer_SSN = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect('../view/' + str(customer_id), code=302)


@app.route('/customers/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New Customers Form')


@app.route('/customers/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('Customer_SSN'), request.form.get('City'), request.form.get('State'),
                 request.form.get('ZipCode'), request.form.get('StreetNum'),
                 request.form.get('CustomerName'), request.form.get('CustomerLogin'), request.form.get('CustomerPassword'))
    sql_insert_query = """INSERT INTO customer (customer_ssn, city, state, zipcode, streetnum, customername, customerlogin, customerpassword)  VALUES (%s, %s,%s, %s,%s, %s,%s, %s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/delete/<int:customer_id>', methods=['POST'])
def form_delete_post(customer_id):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM customer WHERE Customer_SSN = %s """
    cursor.execute(sql_delete_query, customer_id)
    mysql.get_db().commit()
    return redirect("../emphomepage", code=302)


# @app.route('/api/v1/homes', methods=['GET'])
# def api_browse() -> str:
#     cursor = mysql.get_db().cursor()
#     cursor.execute('SELECT * FROM tblhomesImport')
#     result = cursor.fetchall()
#     json_result = json.dumps(result);
#     resp = Response(json_result, status=200, mimetype='application/json')
#     return resp


# @app.route('/api/v1/homes/<int:home_id>', methods=['GET'])
# def api_retrieve(home_id) -> str:
#     cursor = mysql.get_db().cursor()
#     cursor.execute('SELECT * FROM tblhomesImport WHERE id=%s', home_id)
#     result = cursor.fetchall()
#     json_result = json.dumps(result);
#     resp = Response(json_result, status=200, mimetype='application/json')
#     return resp
#
#
# @app.route('/api/v1/homes/<int:home_id>', methods=['PUT'])
# def api_edit(home_id) -> str:
#     cursor = mysql.get_db().cursor()
#     content = request.json
#     inputData = (content['Sell'], content['List'], content['Living'],
#                  content['Rooms'], content['Beds'],
#                  content['Baths'], content['Age'], content['Acres'], content['Taxes'], home_id)
#     sql_update_query = """UPDATE tblhomesImport t SET t.Sell = %s, t.List = %s, t.Living = %s, t.Rooms =
#     %s, t.Beds = %s, t.Baths = %s, t.Age = %s, t.Acres = %s, t.Taxes = %s WHERE t.id = %s """
#     cursor.execute(sql_update_query, inputData)
#     mysql.get_db().commit()
#     resp = Response(status=200, mimetype='application/json')
#     return resp
#
#
# @app.route('/api/v1/homes', methods=['POST'])
# def api_add() -> str:
#     content = request.json
#     cursor = mysql.get_db().cursor()
#     inputData = (content['Sell'], content['List'], content['Living'],
#                  content['Rooms'], content['Beds'],
#                  content['Baths'], content['Age'], content['Acres'], request.form.get('Taxes'))
#     sql_insert_query = """INSERT INTO tblhomesImport (Sell,List,Living,Rooms,Beds,Baths,Age,Acres,Taxes) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) """
#     cursor.execute(sql_insert_query, inputData)
#     mysql.get_db().commit()
#     resp = Response(status=201, mimetype='application/json')
#     return resp
#
#
# @app.route('/api/v1/homes/<int:home_id>', methods=['DELETE'])
# def api_delete(home_id) -> str:
#     cursor = mysql.get_db().cursor()
#     sql_delete_query = """DELETE FROM tblhomesImport WHERE id = %s """
#     cursor.execute(sql_delete_query, home_id)
#     mysql.get_db().commit()
#     resp = Response(status=210, mimetype='application/json')
#     return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
