import requests
import sys


rosterURL = "http://127.0.0.1:5000/exportCourseRoster"
studentsURL = "http://127.0.0.1:5000/exportStudents"


# -----------------------------------------------------------------------------------------------
# A correct case
def test_good():
    data = {
        "courseId": "1521081"
    }
    response = requests.post(rosterURL, json=data)
    assert response.status_code == 200

# -----------------------------------------------------------------------------------------------
# Incorrect course id


def test_bad1():
    data = {
        "courseId": "a"
    }
    response = requests.post(rosterURL, json=data)

    assert response.status_code == 500

# -----------------------------------------------------------------------------------------------
# Incorrect course id


def test_bad2():
    data = {
        "courseId": "1"
    }
    response = requests.post(rosterURL, json=data)
    assert response.status_code == 500

# -----------------------------------------------------------------------------------------------
# Incorrect course id


def test_bad3():
    data = {
        "courseId": 1
    }
    response = requests.post(rosterURL, json=data)
    assert response.status_code == 500

# -----------------------------------------------------------------------------------------------
# Incorrect course id key


def test_bad4():
    data = {
        "course": 1
    }
    response = requests.post(rosterURL, json=data)
    assert response.status_code == 500


def test_KeyGood_Email():
    data = {
        "courseId": "1521081",
        "key": "email"
    }
    response = requests.post(studentsURL, json=data)
    responseMessage = response.json().get('Response')
    goodMessage = [{'id': 4221108, 'email': 'bkieffer04@gmail.com'},
                   {'id': 4340680, 'email': 'harstonj@gmail.com'},
                   {'id': 4221713, 'email': 'smmerz56@gmail.com'}]
    assert goodMessage == responseMessage

def test_KeyGood_Name():
    data = {
        "courseId": "1521081",
        "key": "name"
    }
    
    response = requests.post(studentsURL, json=data)
    responseMessage = response.json().get('Response')
    goodMessage = [{'id': 4221108, 'name': 'bkieffer04@gmail.com'},
                   {'id': 4340680, 'name': 'harstonj@gmail.com'},
                   {'id': 4221713, 'name': 'smmerz56@gmail.com'}]
    assert goodMessage == responseMessage

def test_BadKey1():
    data = {
        "courseId": "1521081",
        "key": ""
    }
    response = requests.post(studentsURL, json=data)
    responseMessage = response.json().get('Response')
    goodMessage = [{'id': 4221108, 'name': 'bkieffer04@gmail.com'},
                   {'id': 4340680, 'name': 'harstonj@gmail.com'},
                   {'id': 4221713, 'name': 'smmerz56@gmail.com'}]
    assert goodMessage == responseMessage

def test_BadKey2():
    data = {
        "courseId": "1521081",
        "key": "cat"
    }
    response = requests.post(studentsURL, json=data)
    responseMessage = response.json().get('Response')
    goodMessage = [{'id': 4221108, 'cat': None},
                   {'id': 4340680, 'cat': None},
                   {'id': 4221713, 'cat': None}]
    assert goodMessage == responseMessage