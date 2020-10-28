 
from flask import Flask, jsonify, request, Response
from database.db import initialize_db
from database.models import Professor, ResearchGroup, Student
import json
from bson.objectid import ObjectId
import os

app = Flask(__name__)

# database configs
app.config['MONGODB_SETTINGS'] = {
    # set the correct parameters here as required, some examples aer give below
    #'host':'mongodb://mongo:27017/<name of db>'
    #'host':'mongodb://localhost/<name of db>'
}
db = initialize_db(app)

# Root
@app.route('/')
def get_route():
    output = {'message': 'It looks like you are trying to access FlaskAPP over HTTP on the native driver port.'}
    return output, 200

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
    elif request.method == "update here":
        # Update Code here

        # Student.objects.get_or_404(id=student_id).delete()
        output = {'message': '', 'id': ''}
        status_code = 000
        return output, status_code


# Complete the  request methods below
@app.route('/listStudent', methods=[]) 
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
    status_code = 000
    return output, status_code

# Only for local testing without docker
#app.run() # FLASK_APP=app.py FLASK_ENV=development flask run