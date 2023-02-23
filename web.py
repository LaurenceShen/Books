import os

from flask import Flask, request, abort, render_template, url_for, flash, redirect
from app_blog import app
from flask_script import Manager, Command, prompt_bool, Shell

from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import configparser
import sqlite3


# config 初始化
config = configparser.ConfigParser()
config.read('config.ini')

books = [['A', 'Allen', '借閱中', '2050/01/01', '25%', '50'], 'B', 'C']
users = {'Me': {'password': 'myself'}}
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
    if tmpuser not in users:
        return

    user = User()
    user.id = tmpuser
    return user

@login_manager.request_loader
def request_loader(request):
    tmpuser = request.form.get('user_id')
    if tmpuser not in users:
        return

    user = User()
    user.id = tmpuser

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form['password'] == users[tmpuser]['password']

    return user


@app.route('/')
def home():
    return redirect(url_for('map'))

@app.route('/map', methods = ['POST', 'GET'])
def map():
    
    return render_template('map.html', bookurl = './noteindex/'+ books[0][0],book = books[0])

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

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template("login.html")

    user_id = request.form['user_id']
    user_password = request.form['password']

    conn = sqlite3.connect('Coding101.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM User;")
    record = cursor.fetchall()

    whe_exist = False
    whe_pass_corr = False
    for i in record:
        if user_id== i[1]:
            whe_exist = True
            print("YES")
        if user_password == i[2]:
            whe_pass_corr = True
            print("yes")
    if whe_exist and whe_pass_corr:
        user = User()
        user.id = user_id
        login_user(user)
        flash(f'{user_id}！開始冒險吧！')
        return redirect(url_for('map'))
    flash('登入失敗了...')
    return render_template('login.html')

    """
    if (user_id in users) and (request.form['password'] == users[user_id]['password']):
        user = User()
        user.id = user_id
        login_user(user)
        flash(f'{user_id}！開始冒險吧！')
        return redirect(url_for('map'))

    flash('登入失敗了...')
    return render_template('login.html')
    """

@app.route('/noteindex/<book>')
def note(book):
    for i in books:
        if i[0] == book:
            output = i
    return render_template('noteindex.html', book = output)

'''
@app.route('/<name>')
def name1(name):
    return render_template('login.html')
'''
'''
@app.route('/<bookname>')
def note1(bookname):
    for i in books:
        if i[0] == bookname:
            return render_template('noteindex.html', book = i)
    return 'not found:('
    #return render_template('noteindex.html', book = )
'''
@app.route('/logout')
def logout():
    user_id = current_user.get_id()
    logout_user()
    flash(f'{user_id}！歡迎下次再來！')
    return render_template('login.html') 

#from app_blog import app
#from app_blog import db
from flask import render_template
#from app_blog.author.model import UserReister
#from app_blog.author.form import FormRegister

import smtplib
server = smtplib.SMTP('smtp.gmail.com',587)

#  import Model
@app.route('/register', methods=['GET', 'POST'])
def register():
    '''
    from model import UserReister
    from form import FormRegister
    form = FormRegister()
    if form.validate_on_submit():
        user = UserReister(
            username = form.username.data,
            email = form.email.data,
            password = form.password.data
        )
        db.session.add(user)
        db.session.commit()
        return 'Success Thank You'
    '''
    if request.method == 'POST':
        name = str(request.values.get('name'))
        password = str(request.values.get('password'))
        print(name.isalpha())
        if name.isalpha() == False:
            flash('請輸入有效id（英文或數字）')
            return render_template('register.html')
        if password.isalpha() == False:
            flash('請輸入有效密碼（英文或數字）')
            return render_template('register.html')
        if name in users.keys():
            flash('用戶已存在')
            return render_template('register.html')
        users[name] = {}
        users[name]['password'] = password
        flash('Success! Please login. user: ' + name)
        return render_template('login.html')


    return render_template('register.html')

app.run(host = '0.0.0.0', port=5000, debug=True)
