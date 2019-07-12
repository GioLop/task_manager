from flask import render_template, flash, redirect, url_for, request, jsonfy
from flask_login  import login_user, current_user, logout_user, login_required
from task_manager import app, db, bcrypt
from task_manager.forms import RegistrationForm, LoginForm
from task_manager.models import User, Board, List, Task

API_V1_PATH = '/api/v1.0'

''' ------ Static routes ------ '''

@app.route('/')
@app.route('/home')
def home():
  if current_user.is_authenticated:
    return redirect(url_for('boards', username=current_user.username))
  else:
    return render_template('home.html')

@app.route('/register')
def register():
    form = RegistrationForm()
    
    if current_user.is_authenticated:
      return redirect(url_for('boards', username=current_user.username))
    else:
      return render_template('register.html', title='Register', form=form)

@app.route('/register', methods=['POST'])
def new_register():
  form = RegistrationForm()

  if form.validate_on_submit():
    hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    user = User(username=form.username.data, email=form.email.data, password=hashed_password)

    db.session.add(user)
    db.session.commit()

    flash('Your account has been created! You are now able to log in', 'success')
    
    return redirect(url_for('login'))
  else:
    return render_template('register.html', title='Register', form=form)  

@app.route('/login', method=['GET'])
def login():
  form = LoginForm()

  if current_user.is_authenticated:
    return redirect(url_for('boards', username=current_user.username))
  else:
    return render_template('login.html', title='Login', form=form)

@app.route('/login', methods=['POST'])
def user_login():
  form = LoginForm()

  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()

    if user and bcrypt.check_password_hash(user.password, form.password.data):
      login_user(user, remember=form.remember.data)   

      return redirect(url_for('boards', username=user.username))         
  else:
    flash('Please check email and password!', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout', method=['GET'])
def logout():
  logout_user()
  return redirect(url_for('home'))

@app.route('/account', method=['GET'])
@login_required
def account():
  return render_template('account.html', current_user=current_user)

@app.route('/<username>/boards')
@login_required
def boards(username):
  return render_template('boards.html', current_user=current_user)

''' ------ API routes ------ '''

'''
  boards = [
    {
      "name": "",
      "id": "" 
    },
    {
      "name": "",
      "id": "" 
    } 
  ]
'''

@app.route(API_V1_PATH + '<int:user_id>/boards/', method=['GET'])
@login_required
def get_board():
  pass

@app.route(API_V1_PATH + '<int:user_id>/boards/', method=['POST'])
@login_required
def add_board():
    pass

@app.route(API_V1_PATH + '<int:user_id>/boards/<int:board_id>', method=['PUT'])
@login_required
def update_board():
    pass

@app.route(API_V1_PATH + '<int:user_id>/boards/<int:board_id>', method=['DELETE'])
@login_required
def delete_board():
    pass

'''
  lists = [
    {
      "name": "",
      "id": "",
      tasks: [
        {
          "name": "",
          "id": ""
        },
        {
          "name": "",
          "id": ""
        }
      ]
    },
    {
      "name": "",
      "id": "",
      tasks: [
        {
          "name": "",
          "id": ""
        },
        {
          "name": "",
          "id": ""
        }
      ] 
    } 
  ]
'''

@app.route(API_V1_PATH + '<int:board_id>/lists')
@login_required
def get_lists():
    pass

@app.route(API_V1_PATH + '<int:board_id>/lists', method=['POST'])
@login_required
def add_list():
    pass

@app.route(API_V1_PATH + '<int:board_id>/lists/<int:list_id>', method=['PUT'])
@login_required
def update_list():
    pass

@app.route(API_V1_PATH + '<int:board_id>/lists/<int:list_id>', method=['DELETE'])
@login_required
def delete_list():
    pass

@app.route(API_V1_PATH + '<int:list_id>/tasks')
@login_required
def get_tasks():
    pass

@app.route(API_V1_PATH + '<int:list_id>/tasks', method=['POST'])
@login_required
def add_tasks():
    pass

@app.route(API_V1_PATH + '<int:list_id>/tasks/<int:task_id>', method=['PUT'])
@login_required
def update_task():
    pass

@app.route(API_V1_PATH + '<int:list_id>/tasks/<int:task_id>', method=['DELETE'])
@login_required
def delete_task():
    pass