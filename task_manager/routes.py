from flask import render_template, flash, redirect, url_for, request
from flask_login  import login_user, current_user, logout_user, login_required
from task_manager import app, db, bcrypt
from task_manager.forms import RegistrationForm, LoginForm, AddBoard, AddList
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
                return render_template('login.html', title='Login', form=form)
        else:
            return render_template('login.html', title='Login', form=form)

@app.route('/account')
@login_required
def account():
    return render_template('account.html', current_user=current_user)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/<username>/boards', methods=['GET', 'POST'])
@login_required
def boards(username):
    form = AddBoard()

    if request.method == 'POST' and form.validate_on_submit():
        new_board = current_user.add_board(name=form.name.data)
        return redirect(url_for('board', board_id=new_board.id))
    else:
        return render_template('boards.html', current_user=current_user, form=form)

@app.route('/b/<int:board_id>', methods=['GET', 'POST'])
@login_required
def board(board_id):
    form = AddList()
    board = Board.query.filter_by(id=int(board_id)).first()

    if request.method == 'POST' and form.validate_on_submit():
        new_list = board.add_list(name=form.name.data)
    
    return render_template('board.html', board=board, form=form)