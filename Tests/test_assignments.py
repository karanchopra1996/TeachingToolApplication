"""Pytest cases for Functions file assignmnets.py"""
import requests, json
import pytest


import requests
f = open("../canvasCredentials.json")
json_object = json.load(f)
canvas_access_token = json_object['token']
f.close()

@pytest.fixture
def authentication_details():
    return {
        "canvas_base_url" : "https://canvas.uw.edu/api/v1/",
        "auth_headers":  {"Authorization": "Bearer {}".format(canvas_access_token)}
    }

assignmentsURL = "http://127.0.0.1:5000/exportAssignments"
assignmentsGoodData = {
    "courseID": "1521081"
}
submissionsURL = "http://127.0.0.1:5000/downloadAssignmentSubmissions"
submissionGoodData = {
    "courseID": "1521081",
    "Assignment_ID" : "8316459"
}

#-----------------------------------------------------------------------------------
# Tests for getAssignments function
def test_Assignment_statusCode_Good():
    response = requests.get(assignmentsURL,  json=assignmentsGoodData)
    
    assert response.status_code == 200

def test_Assignment_statusCode_Bad():
    badURL = "http://127.0.0.1:5000/importAssign"
    response = requests.get(badURL, json=assignmentsGoodData)
    assert response.status_code == 404

def test_Assignment_goodResponse():
    response = requests.get(assignmentsURL, json=assignmentsGoodData)
    responseMessage = response.json().get('Response')
    goodMessage = 'Successfully downloaded all assignments.'
    assert responseMessage == goodMessage

def test_Assignment_badResponse():
    badData = {
        "courseID": "1519021"
    }
    response = requests.get(assignmentsURL, json=badData)
    # responseMessage = response.json().get('Response')
    # goodMessage = 'There was an error finding the course.'
    # assert responseMessage == goodMessage
    assert response.status_code == 500

#----------------------------------------------------------------------------------
#Tests for assignmentSubmissions function
def test_Submission_statusCode_Good():
    response = requests.get(submissionsURL, json=submissionGoodData)
    assert response.status_code == 200


def test_Submission_goodResponse():
    response = requests.get(submissionsURL, json=submissionGoodData)   
    
    responseMessage = response.json().get('Response')
    print(" good message =>", responseMessage)
    goodMessage = 'Successfully downloaded all submissions for assignment: Assignment with submission modes'
    assert responseMessage == goodMessage

def test_Submission_badResponse():
    badData = {
        "courseID": "1521081",
        "Assignment_ID" : "70438912"
    }
    response = requests.get(submissionsURL, json=badData)
    # responseMessage = response.json().get('Response')
    # goodMessage = 'Error at getting Submissions.'
    # assert responseMessage == goodMessage
    assert response.status_code == 500
    
def test_Submission_statusCode_Bad():
    badURL = "http://127.0.0.1:5000/downloadAssignmentSub"
    response = requests.get(badURL, json=submissionGoodData)
    assert response.status_code == 404  
#-----------------------------------------------------------------------------------
def test_get_assignment_metadata(authentication_details):
    """
    Tests for getting the assignment metadata
    """
    courseId = "1521081" 
    assignId = "8316459"
    end_point = authentication_details.get('canvas_base_url')+ "courses/{}/assignments/{}".format(courseId, assignId)
    headers =  authentication_details.get('auth_headers')
    response = requests.get(end_point,   headers = headers)
    assert response.status_code == 200
    
def test_get_submitter_data(authentication_details):
    """
    Tests for getting the submitter data
    """
    end_point = authentication_details.get('canvas_base_url')+ "/users/self/"
    headers =  authentication_details.get('auth_headers')
    response = requests.get(end_point,   headers = headers)
    
    assert response.status_code == 200
    assert "errors" not in response.json()
    assert response.json()['name'] is not None
    assert response.json()['id'] is not None

def test_get_assignment_name(authentication_details):
    """
    Tests for getting theassignment name with course and assignment id
    """
    courseId = "1521081" 
    assignId = "8316459"
    end_point = authentication_details.get('canvas_base_url')+ "/courses/{}/assignments/{}".format(courseId, assignId)
    headers =  authentication_details.get('auth_headers')
    response = requests.get(end_point,   headers = headers)
    
    assert response.status_code == 200
    assert "errors" not in response.json()
    assert response.json()['name'] is not None
    
def test_list_assignments(authentication_details):
    """
    Tests for getting theassignment name with course and assignment id
    """
    courseId = "1521081" 
    assignId = "8316459"
    end_point = authentication_details.get('canvas_base_url')+ "/courses/{}/assignments".format(courseId)
    headers =  authentication_details.get('auth_headers')
    response = requests.get(end_point,   headers = headers)
    assert response.status_code == 200
    assert "errors" not in response.json()
    
def test_get_assignment_metadata_error1(authentication_details):
    """
    Tests for getting the courses 
    """
    courseId = "1521081"
    assignId = "8316459"
    params = { "per_page": "50",
                "include": ['syllabus_body','term'] 
              }
    end_point = authentication_details.get('canvas_base_url')+ "courses//assignments/{}".format(courseId, assignId)
    headers =  authentication_details.get('auth_headers')
    response = requests.get(end_point,   params, headers = headers)
    assert response.status_code == 404
    

def test_get_assignment_metadata_error2(authentication_details):
    """
    Tests for getting the courses 
    """
    courseId = "1521081"
    assignId = "8316459"
    params = { "per_page": "50",
                "include": ['syllabus_body','term'] 
              }
    bad_end_point =  "courses/{}/assignments/{}".format(courseId, assignId)
    headers =  authentication_details.get('auth_headers')
    
    with pytest.raises(ValueError, match= "Invalid URL 'courses/1521081/assignments/8316459'"):
        response = requests.get(bad_end_point,   params, headers = headers)


def test_get_assignment_metadata_error3(authentication_details):
    """
    Tests for getting the courses 
    """
    courseId = "1521081"
    assignId = "8316459"
    params = { "per_page": "50",
                "include": ['syllabus_body','term'] 
              }
    end_point = authentication_details.get('canvas_base_url')+ "courses/{}/assignments/{}".format(courseId, assignId)
    headers =  authentication_details.get('auth_headers')
    response = requests.get(end_point,  params,) 
    assert "errors" in response.json()
    assert response.json()['status'] == "unauthenticated"