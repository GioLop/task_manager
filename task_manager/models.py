from task_manager import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    image_file = db.Column(db.String(120), nullable=False, default='default.jpg')
    boards = db.relationship('Board', backref='user')

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Board(db.Model):
    __tablename__ = 'boards'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    lists = db.relationship('List', backref='board')

    def __repr__(self):
        return f"Board('{self.name}')"

class List(db.Model):
    __tablename__ = 'lists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    board_id = db.Column(db.Integer, db.ForeignKey('boards.id'))
    tasks = db.relationship('Task', backref='list')

    def __repr__(self):
        return f"List('{self.name}')"

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    list_id = db.Column(db.Integer, db.ForeignKey('lists.id'))

    def __repr__(self):
        return f"Task('{self.name}')"
