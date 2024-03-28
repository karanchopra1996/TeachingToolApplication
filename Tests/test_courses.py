import requests, json
import pytest

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
    


def test_get_course(authentication_details):
    """
    Tests for getting a course by courseId 
    """
    courseId = "1521081"
    params = { "per_page": "50",
                "include": ['syllabus_body','term'] 
              }
    end_point = authentication_details.get('canvas_base_url')+ "courses/{}".format(courseId)
    headers =  authentication_details.get('auth_headers')
    response = requests.get(end_point,   params, headers = headers)
    assert response.status_code == 200

def test_get_course_error1(authentication_details):
    """
    Tests for getting a course by courseId 
    """
    courseId = "1521081"
    params = { "per_page": "50",
                "include": ['syllabus_body','term'] 
              }
    bad_end_point = authentication_details.get('canvas_base_url')+ "{}".format(courseId)
    headers =  authentication_details.get('auth_headers')
    response = requests.get(bad_end_point,   params, headers = headers)
    assert response.status_code == 404  

def test_get_course_error2(authentication_details):
    """
    Tests for getting a course by courseId 
    """
    courseId = "1521081"
    params = { "per_page": "50",
                "include": ['syllabus_body','term'] 
              }
    bad_end_point =  "courses/{}".format(courseId)
    headers =  authentication_details.get('auth_headers')
    
    with pytest.raises(ValueError, match= "Invalid URL 'courses/1521081'"):
        response = requests.get(bad_end_point,   params, headers = headers) 

def test_get_course_error3(authentication_details):
    """
    Tests for getting a course by courseId 
    """
    courseId = "1521081"
    params = { "per_page": "50",
                "include": ['syllabus_body','term'] 
              }
    end_point = authentication_details.get('canvas_base_url')+ "courses/{}".format(courseId)
    headers =  authentication_details.get('auth_headers')
    response = requests.get(end_point,   params,) 
    assert "errors" in response.json()
    assert response.json()['status'] == "unauthenticated"
    
def test_get_courses(authentication_details):
    """
    Tests for getting the courses 
    """
    params = { "per_page": "50",
                "include": ['syllabus_body','term'] 
              }
    end_point = authentication_details.get('canvas_base_url')+ "users/self/courses"
    headers =  authentication_details.get('auth_headers')
    response = requests.get(end_point,   params, headers = headers)
    assert response.status_code == 200
    
def test_get_courses_error1(authentication_details):
    """
    Tests for getting the courses 
    """
    params = { "per_page": "50",
                "include": ['syllabus_body','term'] 
              }
    end_point = authentication_details.get('canvas_base_url')+ "users/courses"
    headers =  authentication_details.get('auth_headers')
    response = requests.get(end_point,   params, headers = headers)
    assert response.status_code == 404
    
def test_get_courses_error2(authentication_details):
    """
    Tests for getting the courses 
    """
    params = { "per_page": "50",
                "include": ['syllabus_body','term'] 
              }
    end_point = authentication_details.get('canvas_base_url')+ "users/self/courses"
    headers =  authentication_details.get('auth_headers')
    response = requests.get(end_point,   params)
    print(" error ",response.json() )
    assert response.status_code == 401

def test_get_courses_error3(authentication_details):
    """
    Tests for getting the courses 
    """
    params = { "per_page": "50",
                "include": ['syllabus_body','term'] 
              }
    end_point = "users/self/courses"
    headers =  authentication_details.get('auth_headers')
    
    with pytest.raises(ValueError, match= "Invalid URL 'users/self/courses"):
        response = requests.get(end_point,   params, headers = headers)


def test_get_courses_error4(authentication_details):
    """
    Tests for getting the courses 
    """
    params = { "per_page": "50",
                "include": ['syllabus_body','term'] 
              }
    end_point = authentication_details.get('canvas_base_url')+ "users/self/courses"
    headers =  authentication_details.get('auth_headers')
    response = requests.get(end_point,   params,) 
    assert "errors" in response.json()
    assert response.json()['status'] == "unauthenticated"

    
def test_get_course_students(authentication_details):
    """
    Tests for getting the courses 
    """
    courseId = "1521081"
    params = { "per_page": "50",
                "include": ['syllabus_body','term'] 
              }
    end_point = authentication_details.get('canvas_base_url')+ "courses/{}/students".format(courseId)
    headers =  authentication_details.get('auth_headers')
    response = requests.get(end_point,   params, headers = headers)
    assert response.status_code == 200
    
def test_get_course_students_error1(authentication_details):
    """
    Tests for getting the courses 
    """
    courseId = "1521081"
    params = { "per_page": "50",
                "include": ['syllabus_body','term'] 
              }
    end_point = authentication_details.get('canvas_base_url')+ "courses//students".format(courseId)
    headers =  authentication_details.get('auth_headers')
    response = requests.get(end_point,   params, headers = headers)
    assert response.status_code == 404
    

def test_get_course_students_error3(authentication_details):
    """
    Tests for getting the courses 
    """
    courseId = "1521081"
    params = { "per_page": "50",
                "include": ['syllabus_body','term'] 
              }
    bad_end_point =  "courses/{}/students".format(courseId)
    headers =  authentication_details.get('auth_headers')
    
    with pytest.raises(ValueError, match= "Invalid URL 'courses/1521081/students'"):
        response = requests.get(bad_end_point,   params, headers = headers)


def test_get_course_students_error4(authentication_details):
    """
    Tests for getting the courses 
    """
    courseId = "1521081"
    params = { "per_page": "50",
                "include": ['syllabus_body','term'] 
              }
    end_point = authentication_details.get('canvas_base_url')+ "courses/{}/students".format(courseId)
    headers =  authentication_details.get('auth_headers')
    response = requests.get(end_point,  params,) 
    assert "errors" in response.json()
    assert response.json()['status'] == "unauthenticated"
    