from task_manager import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class BaseModel(db.Model):
    def edit(self, new_name):
        self.name = new_name
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

class User(BaseModel, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    image_file = db.Column(db.String(120), nullable=False, default='default.jpg')
    boards = db.relationship('Board', backref='user')

    def add_board(self, name):
        new_board = Board(name=name, user_id=self.id)
        db.session.add(new_board)
        db.session.commit()
        return new_board

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Board(BaseModel):
    __tablename__ = 'boards'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    lists = db.relationship('List', backref='board')

    def add_list(self, name):
        new_list = List(name=name, board_id=self.id)
        db.session.add(new_list)
        db.session.commit()

    def __repr__(self):
        return f"Board('{self.name}')"

class List(BaseModel):
    __tablename__ = 'lists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    board_id = db.Column(db.Integer, db.ForeignKey('boards.id'), nullable=False)
    tasks = db.relationship('Task', backref='list')

    def add_task(self, name):
        new_task = Task(name=name, list_id=self.id)
        db.session.add(new_task)
        db.session.commit()
    
    def delete_all_tasks(self):
        for task in self.tasks:
            task.delete()

    def __repr__(self):
        return f"List('{self.name}')"

class Task(BaseModel):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    list_id = db.Column(db.Integer, db.ForeignKey('lists.id'))

    def change_list_id(self, new_list_id):
        self.list_id = new_list_id
        db.session.commit()

    def __repr__(self):
        return f"Task('{self.name}')"
