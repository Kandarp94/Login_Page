from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
# app.secret_key = 'your secret key'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'kandarp'
app.config['MYSQL_PASSWORD'] = 'K@ndarp@19'
app.config['MYSQL_DB'] = 'login'

# # Intialize MySQL
mysql = MySQL(app)
#print(mysql)

# http://localhost:5000/accounts/login - this will be the login page, we need to use both GET and POST requests
@app.route('/accounts/login/', methods=['GET', 'POST'])
def login():
    msg = ''
    email=''
    password = ''
    # Check if "email" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        # Create variables for easy access
        email = request.form['email']
        password = request.form['password']

     # Check if account exists using MySQL
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM users WHERE email = %s AND password = %s', (email, password))
    # Fetch one record and return result
    account = cursor.fetchone()
    name = account["first_name"]
        
    # If account exists in accounts table in out database
    if account:
        # Redirect to home page
        return render_template('home.html',username = name)
    else:
        # Account doesnt exist or username/password incorrect
        msg = 'Incorrect username/password!'

    return render_template('index.html', msg=msg)


# http://localhost:5000/accounts/signup - this will be the registration page, we need to use both GET and POST requests
@app.route('/accounts/signup', methods=['GET', 'POST'])
def signup():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'first_name' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']

         # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        account = cursor.fetchone()
        print(account)
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'

        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO users VALUES (NULL, %s, %s, %s, %s, %s)', (first_name, last_name, email, password, phone))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('signup.html', msg=msg)

if __name__ == '__main__':
   app.run(debug = True)