from flask import render_template, flash, redirect, url_for
from task_manager import app
from task_manager.forms import RegistrationForm, LoginForm
from task_manager.models import User, Board, List, Task


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