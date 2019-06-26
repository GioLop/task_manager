import os
from flask import Flask, render_template, flash, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'de8f85a1431dd62d0c4d574a6b08fa08'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/tm.db'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64))
    password = db.Column(db.String(64))
    boards = db.relationship('Board', backref='user')

    def __repr__(self):
        return '<User {0}>'.format(self.name)

class Board(db.Model):
    __tablename__ = 'boards'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    lists = db.relationship('List', backref='board')

    def __repr__(self):
        return '<Board {0}>'.format(self.name)

class List(db.Model):
    __tablename__ = 'lists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    board_id = db.Column(db.Integer, db.ForeignKey('boards.id'))
    tasks = db.relationship('Task', backref='list')

    def __repr__(self):
        return '<List {0}>'.format(self.name)

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    list_id = db.Column(db.Integer, db.ForeignKey('lists.id'))

    def __repr__(self):
        return '<Task {0}>'.format(self.name)

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@taskmanager.com' and form.password.data == '12345_easiest':
            flash('You have been logged in!', 'success')
            return redirect(url_for('boards'))
        else:
            flash('Please check username and password!', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/<username>/boards')
def boards(username):
    return render_template('boards.html', )

if  __name__ == '__main__':
    app.run(debug=True)