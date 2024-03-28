"""Pytest cases for Functions file googleFunctions.py"""

import requests

sharedFolderURL = "http://127.0.0.1:5000/createSharedGoogleFolder"
sharedFolder_data = {
    "courseID": "1521081",
    "parentFolder": [{
        'id': '1u59M_t9FrX2MuiXO294z9bnfjZeiVOXZ',
        'mimeType': 'application/vnd.google-apps.folder',
        'name': 'Teaching Tools Test Files'
    }],
    "roster":
        [{'id': 4221108, 'email': 'ajdeehring@gmail.com'},
         {'id': 4221713, 'email': 'adam.deehring@gmail.com'}],
    "access": "commenter"
}


def test_sharedFolder_Good():
    response = requests.get(sharedFolderURL, json=sharedFolder_data)
    assert response.status_code == 200


def test_sharedFolder_Bad():
    badURL = "http://127.0.0.1:5000/createSharedFolder"
    response = requests.get(badURL, json=sharedFolder_data)
    assert response.status_code == 404


def test_sharedFolder_GoodResponse_pptx():
    response = requests.get(sharedFolderURL, json=sharedFolder_data)
    responseMessage = response.json().get("Response")
    goodMessage = 'Success'
    assert responseMessage == goodMessage


def test_sharedFolder_BadResponse_NoFolder():
    badData = {
        "courseID": "1521081",
        "roster":
        [{'id': 4221108, 'email': 'ajdeehring@gmail.com'},
         {'id': 4221713, 'email': 'adam.deehring@gmail.com'}],
        "access": "commenter"
    }
    response = requests.get(sharedFolderURL, json=badData)
    responseMessage = response.json().get("Response")
    goodMessage = 'Parent Folder was not chosen'
    assert responseMessage == goodMessage


def test_sharedFolder_BadResponse_BadFolder():
    badData = {
        "courseID": "1521081",
        "parentFolder": [{
            'name': 'Teaching Tools Test Files',
            'mimeType': 'application/vnd.google-apps.folder',
        }],
        "roster":
        [{'id': 4221108, 'email': 'ajdeehring@gmail.com'},
         {'id': 4221713, 'email': 'adam.deehring@gmail.com'}],
        "access": "commenter"
    }
    response = requests.get(sharedFolderURL, json=badData)
    responseMessage = response.json().get("Response")
    goodMessage = 'Parent Folder was not chosen'
    assert responseMessage == goodMessage


def test_sharedFolder_BadResponse_FileNotFolder():
    badData = {
        "courseID": "1521081",
        "parentFolder": [{
            'id': '1hy-zLnKQ1YzRk8BEMHNgrM7kyhpvD7taXG5e6qANeZk',
            'mimeType': 'application/vnd.google-apps.presentation',
            'name': 'Teaching Tools Test Slides'
        }],
        "roster":
        [{'id': 4221108, 'email': 'ajdeehring@gmail.com'},
         {'id': 4221713, 'email': 'adam.deehring@gmail.com'}],
        "access": "commenter"
    }
    response = requests.get(sharedFolderURL, json=badData)
    responseMessage = response.json().get("Response")
    goodMessage = "Error: Parent Folder can not be a file"
    assert responseMessage == goodMessage


def test_sharedFolder_BadResponse_NoRoster():
    badData = {
        "courseID": "1521081",
        "parentFolder": [{
            'id': '1u59M_t9FrX2MuiXO294z9bnfjZeiVOXZ',
            'mimeType': 'application/vnd.google-apps.folder',
            'name': 'Teaching Tools Test Files'
        }],
        "roster": [],
        "access": "commenter"
    }
    response = requests.get(sharedFolderURL, json=badData)
    responseMessage = response.json().get("Response")
    goodMessage = 'Roster was not provided'
    assert responseMessage == goodMessage


def test_sharedFolder_BadResponse_NoAccess():
    badData = {
        "courseID": "1521081",
        "parentFolder": [{
            'id': '1u59M_t9FrX2MuiXO294z9bnfjZeiVOXZ',
            'mimeType': 'application/vnd.google-apps.folder',
            'name': 'Teaching Tools Test Files'
        }],
        "roster": [{'id': 4221108, 'email': 'ajdeehring@gmail.com'},
                   {'id': 4221713, 'email': 'adam.deehring@gmail.com'}],
        "access": ""
    }
    response = requests.get(sharedFolderURL, json=badData)
    responseMessage = response.json().get("Response")
    goodMessage = 'Access option was not chosen'
    assert responseMessage == goodMessage


def test_sharedFolder_BadResponse_Bad1Email():
    badData = {
        "courseID": "1521081",
        "parentFolder": [{
            'id': '1u59M_t9FrX2MuiXO294z9bnfjZeiVOXZ',
            'mimeType': 'application/vnd.google-apps.folder',
            'name': 'Teaching Tools Test Files'
        }],
        "roster":
        [{'id': 4221108, 'email': 'ajdeehring@gmail.com'},
         {'id': 4221713, 'email': 'adam.deehring'}],
        "access": "commenter"
    }
    response = requests.get(sharedFolderURL, json=badData)
    responseMessage = response.json().get("Response")
    goodMessage = 'Error: 1 email(s) failed, raised on Following ID(s): 4221713 '
    assert responseMessage == goodMessage


def test_sharedFolder_BadResponse_Bad2Emails():
    badData = {
        "courseID": "1521081",
        "parentFolder": [{
            'id': '1u59M_t9FrX2MuiXO294z9bnfjZeiVOXZ',
            'mimeType': 'application/vnd.google-apps.folder',
            'name': 'Teaching Tools Test Files'
        }],
        "roster":
        [{'id': 4221108, 'email': 'ajdeehring'},
         {'id': 4221713, 'email': 'adam.deehring'}],
        "access": "commenter"
    }
    response = requests.get(sharedFolderURL, json=badData)
    responseMessage = response.json().get("Response")
    goodMessage = 'Error: 2 email(s) failed, raised on Following ID(s): 4221108 4221713 '
    assert responseMessage == goodMessage
