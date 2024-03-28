import requests
import sys


exportStudentGroupsURL = "http://127.0.0.1:5000/exportStudentGroups"
exportGroupsURL = "http://127.0.0.1:5000/exportGroups"
exportGroupURL = "http://127.0.0.1:5000/exportGroup"
exportGroupsGoodData = {
    "courseId": "1521081",
    "key": "email"
}
exportGroupGoodData = {
    "courseId": "1521081",
    "key": "email",
    "teamName": "Team 1"
}

# # Old testing values
# exportGroupsResponseDict = {
#     'Team 0': [{'id': 4221108, 'email': 'bkieffer04@gmail.com'}],
#     'Team 12': [{'id': 4221713, 'email': 'smmerz56@gmail.com'}],
#     'Project Team 1': [],
#     'Project Team 2': [{'id': 4221108, 'email': 'bkieffer04@gmail.com'}],
#     'Project Team 3': [],
#     'Project Team 4': [{'id': 4221713, 'email': 'smmerz56@gmail.com'}],
#     'Project Team 5': [],
#     'Project Team 66': [], 'Team 1': [{'id': 4221108, 'email': 'bkieffer04@gmail.com'}],
#     'Team 2': [],
#     'Team 3': [{'id': 4221713, 'email': 'smmerz56@gmail.com'}],
#     'Team 99': [],
#     'Team 45': [{'id': 4221713, 'email': 'smmerz56@gmail.com'}],
#     'Team 56': [{'id': 4221108, 'email': 'bkieffer04@gmail.com'}],
#     'Team 7': []
# }

# exportGroupsDefaultResponseDict = {
#     'Team 0': [{'id': 4221108, 'name': 'bkieffer04@gmail.com'}],
#     'Team 12': [{'id': 4221713, 'name': 'smmerz56@gmail.com'}],
#     'Project Team 1': [],
#     'Project Team 2': [{'id': 4221108, 'name': 'bkieffer04@gmail.com'}],
#     'Project Team 3': [],
#     'Project Team 4': [{'id': 4221713, 'name': 'smmerz56@gmail.com'}],
#     'Project Team 5': [],
#     'Project Team 66': [], 'Team 1': [{'id': 4221108, 'name': 'bkieffer04@gmail.com'}],
#     'Team 2': [],
#     'Team 3': [{'id': 4221713, 'name': 'smmerz56@gmail.com'}],
#     'Team 99': [],
#     'Team 45': [{'id': 4221713, 'name': 'smmerz56@gmail.com'}],
#     'Team 56': [{'id': 4221108, 'name': 'bkieffer04@gmail.com'}],
#     'Team 7': []
# }

exportGroupsResponseDict = {
    'group 2': [], 
    'my group': [{'id': 4221108, 'email': 'bkieffer04@gmail.com'}, 
                 {'id': 4340680, 'email': 'harstonj@gmail.com'}], 
    'Team 1': [{'id': 4340680, 'email': 'harstonj@gmail.com'}], 
    'Team 2': []
}

exportGroupsDefaultResponseDict = {
    'group 2': [], 
    'my group': [{'id': 4221108, 'name': 'bkieffer04@gmail.com'}, 
                 {'id': 4340680, 'name': 'harstonj@gmail.com'}], 
    'Team 1': [{'id': 4340680, 'name': 'harstonj@gmail.com'}], 
    'Team 2': []
}

# -----------------------------------------------------------------------------------------------
# A correct case
def test_good():
    data = {
        "course": "1521081"
    }
    response = requests.post(exportStudentGroupsURL, json=data)
    assert response.status_code == 200

# -----------------------------------------------------------------------------------------------
# Incorrect course id


def test_bad1():
    data = {
        "course": "a"
    }
    response = requests.post(exportStudentGroupsURL, json=data)
    assert response.status_code == 500

# -----------------------------------------------------------------------------------------------
# Incorrect course id


def test_bad2():
    data = {
        "course": "1"
    }
    response = requests.post(exportStudentGroupsURL, json=data)
    assert response.status_code == 500

# -----------------------------------------------------------------------------------------------
# Incorrect course id


def test_bad3():
    data = {
        "course": 1
    }
    response = requests.post(exportStudentGroupsURL, json=data)
    assert response.status_code == 500

# -----------------------------------------------------------------------------------------------
# Incorrect course id key


def test_bad4():
    data = {
        "courseId": 1
    }
    response = requests.post(exportStudentGroupsURL, json=data)
    assert response.status_code == 500


def test_exportGroups_Good():
    response = requests.get(exportGroupsURL, json=exportGroupsGoodData)
    assert response.status_code == 200


def test_exportGroups_Bad():
    badURL = "http://127.0.0.1:5000/exGroups"
    response = requests.get(badURL, json=exportGroupsGoodData)
    assert response.status_code == 404


def test_exportGroups_GoodResponse():
    response = requests.get(exportGroupsURL, json=exportGroupsGoodData)
    responseMessage = response.json().get("Response")
    assert responseMessage == exportGroupsResponseDict


def test_exportGroups_BadResponse_BadCourse():
    badData = {
        "courseId": "196563",
        "key": "email"
    }
    response = requests.get(exportGroupsURL, json=badData)
    # responseMessage = response.json().get("Response")
    # goodMessage = 'Course was Not Found'
    # assert responseMessage == goodMessage
    assert response.status_code == 500


def test_exportGroups_GoodResponse_DefaultKey():
    badData = {
        "courseId": "1521081",
        "key": ""
    }
    response = requests.get(exportGroupsURL, json=badData)
    responseMessage = response.json().get("Response")
    assert responseMessage == exportGroupsDefaultResponseDict


def test_exportGroup_Good():
    response = requests.get(exportGroupsURL, json=exportGroupsGoodData)
    assert response.status_code == 200


def test_exportGroup_Bad():
    badURL = "http://127.0.0.1:5000/exGroup"
    response = requests.get(badURL, json=exportGroupGoodData)
    assert response.status_code == 404


def test_exportGroup_GoodResponse():
    response = requests.get(exportGroupURL, json=exportGroupGoodData)
    responseMessage = response.json().get("Response")
    goodMessage = [{'id': 4340680, 'email': 'harstonj@gmail.com'}]
    assert responseMessage == goodMessage


def test_exportGroup_BadResponse_BadCourse():
    badData = {
        "courseId": "196563",
        "key": "email",
        "teamName": "Team 1"
    }
    response = requests.get(exportGroupURL, json=badData)
    # responseMessage = response.json().get("Response")
    # goodMessage = 'Course was Not Found'
    # assert responseMessage == goodMessage
    assert response.status_code == 500


def test_exportGroup_BadResponse_BadName():
    badData = {
        "courseId": "1521081",
        "key": "email",
        "teamName": "Team"
    }
    response = requests.get(exportGroupURL, json=badData)
    responseMessage = response.json().get("Response")
    goodMessage = "No Group Found"
    assert responseMessage == goodMessage


def test_exportGroup_GoodResponse_DefaultKey():
    badData = {
        "courseId": "1521081",
        "key": "",
        "teamName": "Team 1"
    }
    response = requests.get(exportGroupURL, json=badData)
    responseMessage = response.json().get("Response")
    goodMessage = [{'id': 4340680, 'name': 'harstonj@gmail.com'}]
    assert responseMessage == goodMessage
