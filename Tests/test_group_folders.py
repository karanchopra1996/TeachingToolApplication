"""Pytest cases for Functions file googleFunctions.py"""

import requests

groupFolderURL = "http://127.0.0.1:5000/createGroupGoogleFolders"


groupFolder_data = {
    "groups": {
        'Team 0': [{'id': 4221108, 'email': 'ajdeehring@gmail.com'}],
        'Team 12': [{'id': 4221713, 'email': 'adam.deehring@gmail.com'}],
        'Project Team 1': [{'id': 4221108, 'email': 'ajdeehring@gmail.com'}],
        'Project Team 2': [{'id': 4221713, 'email': 'adam.deehring@gmail.com'}],
        'Project Team 3': [{'id': 4221108, 'email': 'ajdeehring@gmail.com'}],
        'Project Team 4': [{'id': 4221713, 'email': 'adam.deehring@gmail.com'}],
        'Project Team 5': [{'id': 4221108, 'email': 'ajdeehring@gmail.com'}],
        'Project Team 66': [{'id': 4221713, 'email': 'adam.deehring@gmail.com'}],
        'Team 1': [{'id': 4221108, 'email': 'ajdeehring@gmail.com'}],
        'Team 2': [{'id': 4221713, 'email': 'adam.deehring@gmail.com'}],
        'Team 3': [{'id': 4221108, 'email': 'ajdeehring@gmail.com'}],
        'Team 99': [{'id': 4221713, 'email': 'adam.deehring@gmail.com'}],
        'Team 45': [{'id': 4221108, 'email': 'ajdeehring@gmail.com'}],
        'Team 56': [{'id': 4221713, 'email': 'adam.deehring@gmail.com'}],
        'Team 7': [{'id': 4221108, 'email': 'ajdeehring@gmail.com'}]
    },
    "courseID": "1521081",
    "parentFolder": [{
        'id': '1u59M_t9FrX2MuiXO294z9bnfjZeiVOXZ',
        'mimeType': 'application/vnd.google-apps.folder',
        'name': 'Teaching Tools Test Files'
    }],
    "access": "writer"
}


def test_groupFolder_Good():
    response = requests.get(groupFolderURL, json=groupFolder_data)
    assert response.status_code == 200


def test_sharedFolder_Bad():
    badURL = "http://127.0.0.1:5000/createSharedFolder"
    response = requests.get(badURL, json=groupFolder_data)
    assert response.status_code == 404


def test_sharedFolder_GoodResponse():
    response = requests.get(groupFolderURL, json=groupFolder_data)
    responseMessage = response.json().get("Response")
    goodMessage = 'All Folders Created. 15/15 Group Folders Successfully Shared'
    assert responseMessage == goodMessage


def test_sharedFolder_GoodResponse_IncompleteData():
    nonComplete_data = {
        "groups": {
            'Team 0': [{'id': 4221108, 'email': 'ajdeehring@gmail.com'}],
            'Team 12': [{'id': 4221713, 'email': 'adam.deehring@gmail.com'}],
            'Project Team 1': [],
            'Project Team 2': [{'id': 4221108, 'email': 'ajdeehring@gmail.com'}],
            'Project Team 3': [],
            'Project Team 4': [{'id': 4221713, 'email': 'adam.deehring@gmail.com'}],
            'Project Team 5': [],
            'Project Team 66': [], 'Team 1': [{'id': 4221108, 'email': 'ajdeehring@gmail.com'}],
            'Team 2': [],
            'Team 3': [{'id': 4221713, 'email': 'adam.deehring@gmail.com'}],
            'Team 99': [],
            'Team 45': [{'id': 4221713, 'email': 'adam.deehring@gmail.com'}],
            'Team 56': [{'id': 4221108, 'email': 'ajdeehring@gmail.com'}],
            'Team 7': []
        },
        "courseID": "1521081",
        "parentFolder": [{
            'id': '1u59M_t9FrX2MuiXO294z9bnfjZeiVOXZ',
            'mimeType': 'application/vnd.google-apps.folder',
            'name': 'Teaching Tools Test Files'
        }],
        "access": "writer"
    }
    response = requests.get(groupFolderURL, json=nonComplete_data)
    responseMessage = response.json().get("Response")
    goodMessage = 'All Folders Created. 8/15 Group Folders Successfully Shared'
    assert responseMessage == goodMessage


def test_sharedFolder_BadResponse_BadFolder():
    nonComplete_data = {
        "groups": {
            'Team 0': [{'id': 4221108, 'email': 'ajdeehring@gmail.com'}],
            'Team 12': [{'id': 4221713, 'email': 'adam.deehring@gmail.com'}],
            'Project Team 1': [],
            'Project Team 2': [{'id': 4221108, 'email': 'ajdeehring@gmail.com'}],
            'Project Team 3': [],
            'Project Team 4': [{'id': 4221713, 'email': 'adam.deehring@gmail.com'}],
            'Project Team 5': [],
            'Project Team 66': [], 'Team 1': [{'id': 4221108, 'email': 'ajdeehring@gmail.com'}],
            'Team 2': [],
            'Team 3': [{'id': 4221713, 'email': 'adam.deehring@gmail.com'}],
            'Team 99': [],
            'Team 45': [{'id': 4221713, 'email': 'adam.deehring@gmail.com'}],
            'Team 56': [{'id': 4221108, 'email': 'ajdeehring@gmail.com'}],
            'Team 7': []
        },
        "courseID": "1521081",
        "parentFolder": [{
            'name': 'Teaching Tools Test Files',
            'mimeType': 'application/vnd.google-apps.folder',
        }],
        "access": "writer"
    }
    response = requests.get(groupFolderURL, json=nonComplete_data)
    responseMessage = response.json().get("Response")
    goodMessage = 'Parent Folder was not chosen'
    assert responseMessage == goodMessage


def test_sharedFolder_BadResponse_NotAFolder():
    nonComplete_data = {
        "groups": {
            'Team 0': [{'id': 4221108, 'email': 'ajdeehring@gmail.com'}],
            'Team 12': [{'id': 4221713, 'email': 'adam.deehring@gmail.com'}],
            'Project Team 1': [],
            'Project Team 2': [{'id': 4221108, 'email': 'ajdeehring@gmail.com'}],
            'Project Team 3': [],
            'Project Team 4': [{'id': 4221713, 'email': 'adam.deehring@gmail.com'}],
            'Project Team 5': [],
            'Project Team 66': [], 'Team 1': [{'id': 4221108, 'email': 'ajdeehring@gmail.com'}],
            'Team 2': [],
            'Team 3': [{'id': 4221713, 'email': 'adam.deehring@gmail.com'}],
            'Team 99': [],
            'Team 45': [{'id': 4221713, 'email': 'adam.deehring@gmail.com'}],
            'Team 56': [{'id': 4221108, 'email': 'ajdeehring@gmail.com'}],
            'Team 7': []
        },
        "courseID": "1521081",
        "parentFolder": [{
            'id': '1hy-zLnKQ1YzRk8BEMHNgrM7kyhpvD7taXG5e6qANeZk',
            'mimeType': 'application/vnd.google-apps.presentation',
            'name': 'Teaching Tools Test Slides'
        }],
        "access": "writer"
    }
    response = requests.get(groupFolderURL, json=nonComplete_data)
    responseMessage = response.json().get("Response")
    goodMessage = 'Error: Parent Folder can not be a file'
    assert responseMessage == goodMessage


def test_sharedFolder_BadResponse_NoAccess():
    nonComplete_data = {
        "groups": {
            'Team 0': [{'id': 4221108, 'email': 'ajdeehring@gmail.com'}],
            'Team 12': [{'id': 4221713, 'email': 'adam.deehring@gmail.com'}],
            'Project Team 1': [],
            'Project Team 2': [{'id': 4221108, 'email': 'ajdeehring@gmail.com'}],
            'Project Team 3': [],
            'Project Team 4': [{'id': 4221713, 'email': 'adam.deehring@gmail.com'}],
            'Project Team 5': [],
            'Project Team 66': [], 'Team 1': [{'id': 4221108, 'email': 'ajdeehring@gmail.com'}],
            'Team 2': [],
            'Team 3': [{'id': 4221713, 'email': 'adam.deehring@gmail.com'}],
            'Team 99': [],
            'Team 45': [{'id': 4221713, 'email': 'adam.deehring@gmail.com'}],
            'Team 56': [{'id': 4221108, 'email': 'ajdeehring@gmail.com'}],
            'Team 7': []
        },
        "courseID": "1521081",
        "parentFolder": [{
            'id': '1u59M_t9FrX2MuiXO294z9bnfjZeiVOXZ',
            'mimeType': 'application/vnd.google-apps.folder',
            'name': 'Teaching Tools Test Files'
        }],
        "access": ""
    }
    response = requests.get(groupFolderURL, json=nonComplete_data)
    responseMessage = response.json().get("Response")
    goodMessage = 'Access option was not chosen'
    assert responseMessage == goodMessage
