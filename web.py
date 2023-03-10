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

bag_books = []

conn = sqlite3.connect('Coding101.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM User;")
users = cursor.fetchall()
cursor.close()
conn.close()

current_borrowed = []
Month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
borrowed = {}
bookurl = []
for i in range(30):
    bookurl.append(f"./../noteindex/"+ str(i))
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

#閱讀心得




#print(borrowed)
pjdir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__, static_folder="statics", static_url_path="/")
app.config['SECRET_KEY'] = "Your_secret_string"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#  設置資料庫為sqlite3
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
                                        os.path.join(pjdir, 'data_register.sqlite')
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
cur = []
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
            user.is_authenticated = bcrypt.check_password_hash(i[2],request.form['password'])
            return user
    
    return 

@app.route('/')
def home():
    return redirect(url_for('map'))

@app.route('/map', methods = ['POST', 'GET'])
def map():
    try:
        #current_borrowed = []
        c = []

        stamp = 0
        for j in users:
            if j[1] == current_user.id:
                stamp = j[3]
        print("stamp:", stamp)

        for j in borrowed.values():
            for i in j:
                if i[6] == current_user.id and i[3] == 0:
                    print(i[6])
                    if books[i[1] - 1][0] not in cur:
                        cur.append(books[i[1] - 1][0])
                        current_borrowed.append([books[i[1] - 1][0], books[i[1] - 1][1], books[i[1] - 1][3],  i[4], books[i[1] - 1][4], (i[4]/books[i[1] - 1][4])*100])
                        
        c = current_borrowed.copy()
        c = c[0:2]
        return render_template('map.html', bookurl = bookurl, books = c, bag_books = current_borrowed, stamp = stamp, finish = books)
    except:
        return redirect(url_for('login'))
@app.route('/analysis')
def analysis():
    Category_Book = {}
    conn = sqlite3.connect('Coding101.db')
    cursor = conn.cursor()
    for i in Month:
        sql = """
SELECT * FROM Borrowed_{} INNER JOIN Category_Book ON Category_Book.Book_ID = Borrowed_{}.Book_ID;
        """.format(i, i)
        cursor.execute(sql)
        borrowed_mon = cursor.fetchall()
        Category_Book[i] = borrowed_mon
    cursor.close()
    conn.close()
    preference = [0, 0, 0, 0, 0]
    for i in Category_Book.values():
        for j in i:
            preference[j[6] - 1] += 1
    borrow_size = []
    print("cur: ", current_borrowed)
    for i in borrowed.values():
        borrow_size.append(len(i))
    return render_template('analysis.html', borrow_size = borrow_size, bag_books = current_borrowed, bookurl = bookurl, amount = preference)

@app.route('/post_cards')
def post_cards():
    return render_template('postcards.html', bag_books = current_borrowed, bookurl = bookurl)

@app.route('/mybooks' ,methods=['POST','GET'])
def mybooks():
    conn = sqlite3.connect('Coding101.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Reflection INNER JOIN User ON Reflection.User_ID = User.ID;")
    reflection = cursor.fetchall()
    cursor.close()
    conn.close()
    #將閱讀心得存入字串
    reflection_personal = ""
    thought = {}
    for i in reflection:
        #print(i[1])
        thought[i[1]] = i[3]
        print(thought[i[1]])
    return render_template('mybooks.html', name = "", borrowed = borrowed, books = books, bag_books = current_borrowed, bookurl = bookurl, thought = thought)

@app.route('/discovery', methods = ['POST', 'GET'])
def discovery():
     print(current_borrowed)
     return render_template("discovery.html", books = books, bag_books = current_borrowed, bookurl = bookurl)

@app.route('/donate')
def donate():
    return render_template("donate.html", bag_books = current_borrowed, bookurl = bookurl)

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
    if whe_exist and whe_pass_corr:
        user = User()
        user.id = user_id
        login_user(user)
        flash(f'{user_id}！開始冒險吧！')
        return redirect(url_for('home'))
    flash('登入失敗了...')
    return render_template('login.html')

@app.route('/noteindex/<book>', methods = ['POST', 'GET'])
def note(book):
    cur = []
    current_borrowed = []
    for j in borrowed.values():
            for i in j:
                if i[6] == current_user.id and i[3] == 0:
                    print(i[6])
                    if books[i[1] - 1][0] not in cur:
                        cur.append(books[i[1] - 1][0])
                        current_borrowed.append([books[i[1] - 1][0], books[i[1] - 1][1], books[i[1] - 1][3],  i[4], books[i[1] - 1][4], (i[4]/books[i[1] - 1][4])*100])
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

    conn = sqlite3.connect('Coding101.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Reflection INNER JOIN User ON Reflection.User_ID = User.ID;")
    reflection = cursor.fetchall()
    cursor.close()
    conn.close()
    #將閱讀心得存入字串
    reflection_personal = ""
    for i in reflection:
        print(i[2])
        if int(book) == i[1] and current_user.id == i[6]:
            reflection_personal = i[3]
    print("hi:", reflection_personal)
    if request.method == 'POST':
        if 'bookprogress' in request.form.keys():
            mon = ""
            for i in borrowed.keys():
                for j in borrowed[i]:
                    if int(book) == j[1] and current_user.id == j[6]:
                        mon = i
            conn = sqlite3.connect('Coding101.db')
            cursor = conn.cursor()
            sql = """
UPDATE Borrowed_{} SET Page_SoFar = {} WHERE Book_ID = {};
        """.format(mon, request.form['bookprogress'], int(book))
            cursor.execute(sql)
            conn.commit()
            print('page:', request.form['bookprogress'])
        else:
            conn = sqlite3.connect('Coding101.db')
            cursor = conn.cursor()
            sql = """
INSERT INTO Reflection (Book_ID, User_ID, Reflection, Rate)
VALUES({}, 1, \'{}\', 5);
        """.format(int(book), request.form['thought'])
            cursor.execute(sql)
            conn.commit()
            print('thought:', request.form['thought'])
    output = None
    for i in books:
        #print(i[0])
        if i[0] == int(book):
            output = list(i)
    if (output == None):
        return render_template('error.html')
    for i in current_borrowed:
        if i[0] == output[0]:
            output.append(i[3])
    return render_template('noteindex.html', book = output, bag_books = current_borrowed, bookurl = bookurl, thought = reflection_personal)

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
        INSERT INTO User (User_Name, Password, Stamp, Postcard)
        VALUES (\"{}\", \"{}\", 0, 0);
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