 
from flask import Flask, jsonify, request, Response
from database.db import initialize_db
from database.models import Professor, ResearchGroup, Student
import json
from bson.objectid import ObjectId
import os

app = Flask(__name__)

# database configs
app.config['MONGODB_SETTINGS'] = {
    'host':'mongodb://mongo:27017/flask-db'
    # 'host':'mongodb://localhost/flask-db'
}

db = initialize_db(app)

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
    return { 'message': 'Professor successfully created', 'id': str(id)}, 201

# Get a single professor by id
@app.route('/listProfessor/<prof_id>', methods=['GET'])
def get_professor_by_id(prof_id):
    prof = Professor.objects.get(id=prof_id)
    output = { 'name': str(prof.name), 'email': str(prof.email), 'designation': str(prof.designation), 'interests': prof.interests}
    return output, 200

# Get a list of professors (potentially filter by designation or groupName)
@app.route('/listProfessors', methods=['GET'])
def get_professors():
    groupName = request.args.get('groupName')
    designation = request.args.get('designation')
    all_prof = {}

    if designation:
        all_prof = Professor.objects(designation=designation)
    elif group:
        # all_prof = Professor.objects(designation=designation)
        all_prof = Professor.objects(researchGroups__name=groupName)

    output = [{'name': str(p['name']), 'email': str(p['email'])} for p in all_prof]
    return jsonify(output), 200

# Update professor
@app.route('/listProfessor/<prof_id>', methods=['PUT'])
def update_professor(prof_id):
    body = request.get_json()
    Professor.objects.get(id=prof_id).update(**body)
    return { 'message': 'Professor successfully update', 'id': str(prof_id)}, 200

# Delete professor
@app.route('/listProfessor/<prof_id>', methods=['DELETE'])
def delete_professor(prof_id):
    Professor.objects.get_or_404(id=prof_id).delete()
    return { 'message': 'Professor successfully deleted', 'id': str(prof_id)}, 200

# - - - - - - - Routes for research groups - - - - - - - 

# Create research group
@app.route('/listGroup', methods=['POST'])
def add_group():
    body = request.get_json()
    group = ResearchGroup(**body).save()
    id = group.id
    output = { 'message': 'Group successfully created', 'id': str(id)}
    return output, 201

@app.route('/listGroup/<group_id>', methods=['GET'])
def get_group_by_id(group_id):
    group = ResearchGroup.objects.get(id=group_id)
    founder = group.founder.id
    output =  { 'id': str(group.id), 'name': str(group.name), 'founder': str(founder) }
    return output, 200

@app.route('/listGroup/<group_id>', methods=['PUT'])
def update_group(group_id):
    body = request.get_json()
    ResearchGroup.objects.get(id=group_id).update(**body)
    output = { 'message': 'Group successfully updated', 'id': str(group_id)}
    status = 200
    return output, status

@app.route('/listGroup/<group_id>', methods=['DELETE'])
def delete_group(group_id):
    ResearchGroup.objects.get_or_404(id=group_id).delete()
    output = { 'message': 'Group successfully deleted', 'id': str(group_id)}
    return output, 200

# - - - - - - - Routes for students - - - - - - - 

# Update the methods below
@app.route('/listStudent/<student_id>', methods=['GET', 'PUT'])
def get_student_by_id(student_id):
    """
    Get (read), update or delete a student

    Args:
        student_id (Object id): The student Id of the student record that nees to be modified.

    Returns:
        dict: The dictionary with output values
        int : The status code
    """
    
    if request.method == "GET":
        student = Student.objects.get_or_404(id=student_id)
        if student:
            name = student.name
            studentNumber = student.studentNumber
            groups = student.researchGroups
            output = {'name': str(name), 'studentNumber': str(studentNumber), 'researchGroups': groups }
            status_code = 200
        else:
            output = {'message': 'Student not found'}
            status_code = 404
        return output, status_code
    elif request.method == "PUT":
        body = request.get_json()
        keys = body.keys()
        output = {}
        if body and keys:
            for key in keys:
                student.update(key=body[key])
            output = {'message': 'Student succesfully updated', 'id': str(student.id)}
        else:
            # Update Code here
            output = {'message': 'Message body empty'}
        status_code = 200
        return output, status_code


@app.route('/listStudent/<student_id>', methods=['DELETE'])
def delete_student(student_id):
    Student.objects.get_or_404(id=student_id).delete()
    output = {'message': 'Student successfully deleted', 'id': str(student_id)}
    status_code = 200
    return output, status_code


@app.route('/listStudents', methods=['GET'])
def get_students():
    groupName = request.args.get('groupName')
    students = Student.objects(researchGroups__name=groupName)

    output = [{'name': str(s['name']), 'studentNumber': str(s['studentNumber'])} for s in students]
    return jsonify(output), 200


# Complete the  request methods below
@app.route('/listStudent', methods=['POST']) 
def add_student():
    """
    This function creates a new student given student_id in the request body

    Returns:
        dict: Dictionary containing the message and id
        int : The status code
    """
    body = request.get_json()
    student = Student(**body).save()
    id = student.id
    output = {'message': "Student successfully created", 'id': str(id)}
    # Update the status code
    status_code = 201
    return output, status_code

# Only for local testing without docker
#app.run() # FLASK_APP=app.py FLASK_ENV=development flask run