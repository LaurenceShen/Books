import os

from flask import Flask, request, abort, render_template, url_for, flash, redirect

from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import configparser


# config 初始化
config = configparser.ConfigParser()
config.read('config.ini')

books = ['A', 'B', 'C']
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
def user_loader(使用者):
    if 使用者 not in users:
        return

    user = User()
    user.id = 使用者
    return user

@login_manager.request_loader
def request_loader(request):
    使用者 = request.form.get('user_id')
    if 使用者 not in users:
        return

    user = User()
    user.id = 使用者

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form['password'] == users[使用者]['password']

    return user


@app.route('/')
def home():
    return redirect(url_for('map'))

@app.route('/map')
def map():
    return render_template('map.html')

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
    return render_template("ryan_discovery.html", books = books)

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template("login.html")

    user_id = request.form['user_id']
    if (user_id in users) and (request.form['password'] == users[user_id]['password']):
        user = User()
        user.id = user_id
        login_user(user)
        flash(f'{user_id}！開始冒險吧！')
        return redirect(url_for('map'))

    flash('登入失敗了...')
    return render_template('login.html')

@app.route('./noteindex')
def note():
    return render_template('noteindex.html')

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

#  import Model
@app.route('/register', methods=['GET', 'POST'])
def register():
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
    return render_template('register.html', form=form)

app.run(host = '0.0.0.0', port=5000, debug=True)
