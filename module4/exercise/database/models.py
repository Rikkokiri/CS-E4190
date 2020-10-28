from .db import db

class Professor(db.Document):
    name = db.StringField(max_length=20,required=True, unique=True)
    # complete the remaining code
    

class ResearchGroup(db.Document):
    name = "fill here"
    # complete the remaining code

class Student(db.Document):
    name = "fill here"
    # complete the remaining code
