from flask import Flask, render_template, redirect, jsonify, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, current_user, AnonymousUserMixin
from datetime import datetime
import jinja2
import sqlalchemy
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import OpenSSL


app = Flask(__name__)
app.config['SECRET_KEY'] = 'zbnjlbrkns'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

engine = sqlalchemy.create_engine('sqlite:///db.sqlite3',connect_args={'check_same_thread': False})
session = sessionmaker(bind=engine)()
base = declarative_base()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    joindate = db.Column(db.DateTime, default=datetime.now)
    def check_password(self, password, checkpassword):
        if password == checkpassword:
            return True
        else:
            return False

class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    time= db.Column(db.DateTime, default=datetime.now)
    tier = db.Column(db.Integer)
    title = db.Column(db.String(999), default="Untitled")
    text = db.Column(db.String(9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999))
    
class LoginForm(FlaskForm):
    username = StringField('username')
    password = PasswordField('password')

class generalform(FlaskForm):
    text = StringField('text')
    text2 = StringField('text2')
    text3 = StringField('text3')
    text4 = StringField('text4')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def home():
    if not current_user.is_authenticated:
        return render_template("home.html", username='Guest')
    else:
        return render_template("home.html", username= current_user.username)

@app.route('/notes', methods=['GET','POST'])
def notes():
    form = generalform()
    if form.validate_on_submit():
        if form.text3.data == "new":
            text = form.text.data
            title=form.text2.data
            text = text.replace('&lt;img', '<img').replace('&gt;', '>').replace('<script', '&lt;script')
            title = title.replace('&lt;img', '<img').replace('&gt;', '>').replace('<script', '&lt;script')
            note = Notes(username = current_user.username, text= text, title=title)
            db.session.add(note)
            db.session.commit()
        else:
            note = Notes.query.get(int(form.text3.data))
            if note == None or note.username != current_user.username:
                return render_template("wrong note")
            else:
                text = form.text.data
                title=form.text2.data

                text = text.replace('&lt;img', '<img').replace('&gt;', '>').replace('<script', '&lt;script')
                title = title.replace('&lt;img', '<img').replace('&gt;', '>').replace('<script', '&lt;script')
                note.text = text
                note.title = title
                db.session.commit()
            
    if not current_user.is_authenticated:
        return "log in to use notes"
    else:
        notestext=[]
        notesids=[]
        usernotes = Notes.query.filter_by(username=current_user.username).all()
        for note in usernotes:
            notestext.append(note.title)
            notesids.append(note.id)
        print(notesids)
        print(notestext)

        return render_template("notes.html", form=form, notestext=notestext, notesids=notesids, title="New Note", text="I'm thinking about...", currentid="new")

@app.route('/notes/<noteid>')
def noteselected(noteid):
    form = generalform()
    if form.validate_on_submit():
        note = Notes.query.get(int(form.text3.data))
        if note == None or note.username != current_user.username:
            return render_template("wrong note")
        else:
            text = form.text.data
            title=form.text2.data
            text = text.replace('&lt;img', '<img').replace('&gt;', '>').replace('<script', '&lt;script')
            title = title.replace('&lt;img', '<img').replace('&gt;', '>').replace('<script', '&lt;script')
            note.text = text
            note.title= title
            db.session.commit()
    if not current_user.is_authenticated:
        return "log in to use notes"
    else:
        selectednote = Notes.query.filter_by(id=noteid, username=current_user.username).first()
        notestext=[]
        notesids=[]
        usernotes = Notes.query.filter_by(username=current_user.username).all()
        for note in usernotes:
            notestext.append(note.title)
            notesids.append(note.id)
        return render_template("notes.html", form=form, notestext=notestext, notesids=notesids, title=selectednote.title,currentid=noteid, text=selectednote.text)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = LoginForm()
    if form.validate_on_submit():
        user = User(username = form.username.data, password = form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect("/", code=302)
    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def loginform():
    loginform = LoginForm()
    if loginform.validate_on_submit():
        try:
            user = User.query.filter_by(username=loginform.username.data).first()
            if user.check_password(user.password, loginform.password.data):
                login_user(user)
                return redirect("/", code=302)
            else:
                pass
        except:
            pass
        
    return render_template('login.html',form=loginform)
if __name__ == '__main__':
     app.debug = True
     app.run()#ssl_context='adhoc'