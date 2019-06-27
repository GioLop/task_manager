from flask import render_template, flash, redirect, url_for
from flask_login  import login_user, current_user, logout_user
from task_manager import app, db, bcrypt
from task_manager.forms import RegistrationForm, LoginForm
from task_manager.models import User, Board, List, Task


@app.route('/')
@app.route('/home')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('boards', username=current_user.username))
    else:
        return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    
    if current_user.is_authenticated:
        return redirect(url_for('boards', username=current_user.username))
    else:
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data, email=form.email.data, password=hashed_password)

            db.session.add(user)
            db.session.commit()

            flash('Your account has been created! You are now able to log in', 'success')
            
            return redirect(url_for('login'))
        else:
            return render_template('register.html', title='Register', form=form) 

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if current_user.is_authenticated:
        return redirect(url_for('boards', username=current_user.username))
    else:
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()

            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)   

                return redirect(url_for('boards', username=user.username))         
            else:
                flash('Please check email and password!', 'danger')
        else:
            return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/<username>/boards')
def boards(username):
    return render_template('boards.html', username=username ) 