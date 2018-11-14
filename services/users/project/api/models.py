# services/users/project/api/models.py
from sqlalchemy.sql import func

from flask_login import UserMixin

from project import login_manager
from project import db

# model
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)
    date_of_joining = db.Column(db.DateTime(timezone=True))
    dob = db.Column(db.Date())
    branch = db.Column(db.String(128))
    role = db.Column(db.String(128))

class Student(User):

    usn = db.Column(db.String(128))
    semester = db.Column(db.Integer)
    section = db.Column(db.String(2))

    def __init__(self, usn, name, email, branch, semester, section):
        self.usn = usn
        self.name = name
        self.email = email
        self.branch = branch
        self.semester = semester
        self.section = section 
        self.role = "Student"

class Teacher(User):

    f_id = db.Column(db.String(128))
    position = db.Column(db.String(128))

    def __init__(self, f_id, name, email, branch, position):
        self.f_id = f_id
        self.name = name
        self.email = email
        self.branch = branch
        self.position = position
        self.role = "Teacher"


# @login_manager.user_loader
# def load_user(id):
#     return User.query.get(int(id))