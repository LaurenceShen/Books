import os

from flask import Flask, request, abort, render_template, url_for, flash, redirect
from flask_script import Manager, Command, prompt_bool, Shell
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
#from app_blog import app
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import configparser
import sqlite3


# config 初始化
config = configparser.ConfigParser()
config.read('config.ini')

conn = sqlite3.connect('Coding101.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM Library;")
books = cursor.fetchall()
cursor.close()
conn.close()

conn = sqlite3.connect('Coding101.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM User;")
users = cursor.fetchall()
cursor.close()
conn.close()

Month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
borrowed = {}
conn = sqlite3.connect('Coding101.db')
cursor = conn.cursor()
for i in Month:
    sql = """
SELECT * FROM Borrowed_{} INNER JOIN User ON User.ID = Borrowed_{}.User_ID
    """.format(i, i)
    cursor.execute(sql)
    borrowed_mon = cursor.fetchall()
    borrowed[i] = borrowed_mon
cursor.close()
conn.close()


pjdir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__, static_folder="statics", static_url_path="/")
app.config['SECRET_KEY'] = "Your_secret_string"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#  設置資料庫為sqlite3
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
                                        os.path.join(pjdir, 'data_register.sqlite')
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"
login_manager.login_view = 'login'
login_manager.login_message = 'login_message'
class User(UserMixin):
    pass

@login_manager.user_loader
def user_loader(tmpuser):
    for i in users:
        if tmpuser == i[1]:
            user = User()
            user.id = tmpuser
            return user
    return 

@login_manager.request_loader
def request_loader(request):
    tmpuser = request.form.get('user_id')
    for i in users:
        if tmpuser == i[1]:
            user = User()
            user.id = tmpuser
            user.is_authenticated = request.form['password'] == users[tmpuser]['password']
            return user
    
    return 

@app.route('/')
def home():
    return redirect(url_for('map'))

@app.route('/map', methods = ['POST', 'GET'])
def map():
    
    return render_template('map.html', bookurl = './noteindex/'+ str(books[0][0]), book = books[0], bag = borrowed)

@app.route('/post_cards')
def post_cards():
    return render_template('post_cards.html')

@app.route('/mybooks' ,methods=['POST','GET'])
def mybooks():
    if request.method =='POST':
        if request.values['send']=='探索':
            return render_template('mybooks.html', name = request.values['mybook'])
    return render_template('mybooks.html', name = "")

@app.route('/discovery', methods = ['POST', 'GET'])
def discovery():
    return render_template("discovery.html", books = books)

@app.route('/donate')
def donate():
    return render_template("donate.html")

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template("login.html")

    user_id = request.form['user_id']
    user_password = request.form['password']

    whe_exist = False
    whe_pass_corr = False
    
    for i in users:
        if user_id == i[1] and bcrypt.check_password_hash(i[2], user_password):
            whe_exist = True
            whe_pass_corr = True
        print(bcrypt.check_password_hash(i[2], user_password))
        print(i[1])
    if whe_exist and whe_pass_corr:
        user = User()
        user.id = user_id
        login_user(user)
        flash(f'{user_id}！開始冒險吧！')
        return redirect(url_for('map'))
    flash('登入失敗了...')
    return render_template('login.html')

@app.route('/noteindex/<book>')
def note(book):
    output = None
    for i in books:
        #print(i[0])
        if i[0] == int(book):
            output = i
            print(':(')
    return render_template('noteindex.html', book = output)

@app.route('/logout')
def logout():
    user_id = current_user.get_id()
    logout_user()
    flash(f'{user_id}！歡迎下次再來！')
    return render_template('login.html') 

from flask import render_template

import smtplib
server = smtplib.SMTP('smtp.gmail.com',587)

#  import Model
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = str(request.values.get('name'))
        password = str(request.values.get('password'))
        if name.isalnum() == False:
            flash('請輸入有效id（英文或數字）')
            return render_template('register.html')
        if password.isalnum() == False:
            flash('請輸入有效密碼（英文或數字）')
            return render_template('register.html')
        conn = sqlite3.connect('Coding101.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM User;")
        record = cursor.fetchall()

        whe_exist = False
        for i in record:
            if name == i[1]:
                whe_exist = True
        if whe_exist:
            flash('用戶已存在')
            return render_template('register.html')
        password = bcrypt.generate_password_hash(password).decode('utf-8')
        print(type(password))
        sql = """
        INSERT INTO User (User_Name, Password, Stamp, Postcard1, Postcard2, Postcard3, Postcard4, Postcard5, Postcard6, Postcard7, Postcard8, Postcard9, Postcard10, Postcard11, Postcard12, Postcard13, Postcard14, Postcard15, Postcard16, Postcard17, Cat1, Cat2, Cat3, Cat4, Cat5, Cat6, Cat7, Cat8, Cat9, Cat10, Cat11, Cat12, Cat13, Cat14, Cat15, Cat16, Cat17)
        VALUES (\"{}\", \"{}\", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
        """.format(name, password)
        cursor.execute(sql)
        conn.commit()
        flash('Success! Please login. user: ' + name)
        print(users)
        return render_template('login.html')
        cursor.close()
        conn.close()
    return render_template('register.html')

app.run(host = '0.0.0.0', port=5000, debug=True)
