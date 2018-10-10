# services/users/project/api/models.py
from sqlalchemy.sql import func

from project import db

# model
class Student(db.Model):
    __tablename__ = 'student'
    usn = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    branch = db.Column(db.String(128), nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    section = db.Column(db.String(2), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)
    
    def __init__(self, usn, name, email, branch, semester, section):
        self.usn = usn
        self.name = name
        self.email = email
        self.branch = branch
        self.semester = semester
        self.section = section 
