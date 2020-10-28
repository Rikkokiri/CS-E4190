 
from flask import Flask, jsonify, request, Response
from database.db import initialize_db
from database.models import Professor, ResearchGroup, Student
import json
from bson.objectid import ObjectId
import os

app = Flask(__name__)

# database configs
app.config['MONGODB_SETTINGS'] = {
    # 'host':'mongodb://mongo:27017/flask-db'
    'host':'mongodb://localhost/flask-db'
}

# db = initialize_db(app)
initialize_db(app)

# Root
@app.route('/')
def get_route():
    output = {'message': 'It looks like you are trying to access FlaskAPP over HTTP on the native driver port.'}
    return output, 200

# - - - - - - - Routes for professors - - - - - - - 

# Create a professor
@app.route('/listProfessor', methods=['POST'])
def add_professor():
    body = request.get_json()
    prof = Professor(**body).save()
    id = prof.id
    return { 'message': 'Professor successfully created', 'id': str(id)}, 200

# Get a single professor by id
@app.route('/listProfessor/<prof_id>', methods=['GET'])
def get_professor_by_id(prof_id):
    return 'TODO', 200

# Get a list of professors (potentially filter by designation or groupName)
@app.route('/listProfessors', methods=['GET'])
def get_professors():
    # group = request.args.get('group')
    return 'TODO', 200

# Update professor
@app.route('/listProfessor/<prof_id>', methods=['PUT'])
def update_professor(prof_id):
    body = request.get_json()
    prof = Professor.objects.get(id=prof_id)
    prof.update(**body)
    return { 'message': 'Professor successfully update', 'id': str(prof.id)}, 200

# Delete professor
@app.route('/listProfessor/<prof_id>', methods=['DELETE'])
def delete_professor(prof_id):
    prof = Professor.objects.get_or_404(id=prof_id).delete()
    return { 'message': 'Professor successfully deleted', 'id': str(prof_id)}, 200

# - - - - - - - Routes for research groups - - - - - - - 

# Create research group
@app.route('/listGroup', methods=['POST'])
def add_group():
    body = request.get_json()
    group = ResearchGroup(**body).save()
    id = group.id
    output = { 'message': 'Group successfully created', 'id': str(id)}
    return output, 200

@app.route('/listGroup/<group_id>', methods=['GET'])
def get_group_by_id(group_id):
    output =  { 'id': '', 'name': '', 'founder': '' }
    status = 200
    return output, status

@app.route('/listGroup/<group_id>', methods=['PUT'])
def update_group(group_id):
    output = { 'message': 'Group successfully updated', 'id': ''}
    status = 200
    return output, status

@app.route('/listGroup/<group_id>', methods=['DELETE'])
def delete_group(group_id):
    output = { 'message': 'Group successfully deleted', 'id': ''}
    status = 200
    return output, status


# - - - - - - - Routes for students - - - - - - - 

# Update the methods below
@app.route('/listStudent/<student_id>', methods=[])
def get_student_by_id(student_id):
    """
    Get (read), update or delete a student

    Args:
        student_id (Object id): The student Id of the student record that nees to be modified.

    Returns:
        dict: The dictionary with output values
        int : The status code
    """
    
    if request.method == "Update here":
        student = "Get the students from database here"
        if student:
            # Update Code here
            
            output = {'name': "", 'studentNumber': "", 'researchGroups': ""}
        else:
            # Update Code here
            
            output = {'message': ''}
        status_code = 000
        return output, status_code
    elif request.method == "Update this line":
        body = request.get_json()
        keys = body.keys()
        if body and keys:
            # Update Code here
            
            output = {'message': '', 'id': ''}
        else:
            # Update Code here
            
            output = {'message': 'Message body empty'}
        status_code = 000
        return output, status_code
    elif request.method == "DELETE":
        Student.objects.get_or_404(id=student_id).delete()
        output = {'message': 'Student successfully deleted', 'id': str(student_id)}
        status_code = 200
        return output, status_code


# Complete the  request methods below
@app.route('/listStudent', methods=['POST']) 
def add_student():
    """
    This function creates a new student given student_id in the request body

    Returns:
        dict: Dictionary containing the message and id
        int : The status code
    """

    # Update the code here.      

    output = {'message': "", 'id': ""}
    # Update the status code
    status_code = 200
    return output, status_code

# Only for local testing without docker
#app.run() # FLASK_APP=app.py FLASK_ENV=development flask run