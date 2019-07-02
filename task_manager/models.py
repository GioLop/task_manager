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

    def add_board(self, name):
        new_board = Board(name=name, user_id=self.id)
        db.session.add(new_board)
        db.session.commit()
        return new_board
    
    def remove_board(self, name):
        board = Board.query.filter_by(name=name).first()
        db.session.delete(board)
        db.session.commit()

class Board(db.Model):
    __tablename__ = 'boards'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    lists = db.relationship('List', backref='board')

    def __repr__(self):
        return f"Board('{self.name}')"

    def add_list(self, name):
        new_list = List(name=name, board_id=self.id)
        db.session.add(new_list)
        db.session.commit()

class List(db.Model):
    __tablename__ = 'lists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    board_id = db.Column(db.Integer, db.ForeignKey('boards.id'))
    tasks = db.relationship('Task', backref='list')

    def __repr__(self):
        return f"List('{self.name}')"
    
    def add_task(self, name):
        new_task = Task(name=name, list_id=self.id)
        db.session.add(new_task)
        db.session.commit()

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    list_id = db.Column(db.Integer, db.ForeignKey('lists.id'))

    def __repr__(self):
        return f"Task('{self.name}')"

    def move_task(self):
        pass
    
    def change_name(self):
        pass
    
    def delete(self):
        pass