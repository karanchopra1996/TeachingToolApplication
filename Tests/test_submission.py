"""Pytest cases for Functions file canvasAssignments.py"""
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
    
def test_get_submission_error(authentication_details):
    courseId = "1521081" 
    assignId = "8316459"
    headers = authentication_details.get('auth_headers')
    end_point = "/courses/{}/assignments/{}/submissions".format(courseId,assignId)
    
    
    with pytest.raises(ValueError):
        response = requests.get(end_point,   headers = headers)
        
def test_get_submission(authentication_details):
    courseId = "1521081" 
    assignId = "8316459"
    headers = authentication_details.get('auth_headers')
    end_point = authentication_details.get('canvas_base_url')+ "/courses/{}/assignments/{}/submissions".format(courseId,assignId)
    
   
    response = requests.get(end_point,   headers = headers)
    assert response.status_code == 200
    
def test_get_submission(authentication_details):
    courseId = "1521081" 
    assignId = "8316459"
    params = { "per_page": "50",
                "include": ['syllabus_body','term'] 
              }
    headers = authentication_details.get('auth_headers')
    end_point = authentication_details.get('canvas_base_url')+ "/courses/{}/assignments/{}/submissions".format(courseId,assignId)
    
   
    response = requests.get(end_point,   headers = headers, params = params)
    assert response.status_code == 200
    
def test_get_submission_error2(authentication_details):
    courseId = "1521081" 
    assignId = "8316459"
    headers = authentication_details.get('auth_headers')
    end_point = authentication_details.get('canvas_base_url')+ "/courses/{}/assignments/{}/submissions".format(courseId,assignId)
    response = requests.get(end_point,   headers = headers)
    assert "syllabus_body" not in response
         
    
    