from .db import db

DESIGNATIONS = ['Professor', 'Assistant Professor', 'Associate Professor']

class Professor(db.Document):
    name = db.StringField(max_length=20,required=True, unique=True)
    designation = db.StringField(choices = DESIGNATIONS, required=True)
    email = db.StringField()
    interests = db.ListField(db.StringField(), default=list)
    researchGroups = db.ListField(db.ReferenceField('ResearchGroup'))

class ResearchGroup(db.Document):
    name = db.StringField(max_length=20,required=True, unique=True)
    description = db.StringField()
    founder = db.ReferenceField(Professor, required=True)

class Student(db.Document):
    name = db.StringField(max_length=20,required=True, unique=True)
    studentNumber = db.StringField(required=True, unique=True)
    researchGroups = db.ListField(db.ReferenceField(ResearchGroup))
