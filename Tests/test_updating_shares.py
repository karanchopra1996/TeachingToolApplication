"""Pytest cases for Functions file googleFunctions.py"""

import requests

updateSharesURL = "http://127.0.0.1:5000/updateSharesOnFolder"

updateShares_data = {
    "file": [{
        'id': '1hy-zLnKQ1YzRk8BEMHNgrM7kyhpvD7taXG5e6qANeZk',
        'mimeType': 'application/vnd.google-apps.presentation',
        'name': 'Teaching Tools Test Slides'
    }],
    "roster":
        [{'id': 4221108, 'email': 'ajdeehring@gmail.com'},
         {'id': 4221713, 'email': 'adam.deehring@gmail.com'}],
    "access": "commenter"
}


def test_updateShares_Good():
    response = requests.get(updateSharesURL, json=updateShares_data)
    assert response.status_code == 200


def test_updateShares_Bad():
    badURL = "http://127.0.0.1:5000/updateShares"
    response = requests.get(badURL, json=updateShares_data)
    assert response.status_code == 404


def test_updateShares_GoodResponse_pptx():
    response = requests.get(updateSharesURL, json=updateShares_data)
    responseMessage = response.json().get("Response")
    goodMessage = 'Success'
    assert responseMessage == goodMessage


def test_updateShares_BadResponse_NoFile():
    badData = {
        "file": [{
            'name': 'Teaching Tools Test Slides'
        }],
        "roster":
        [{'id': 4221108, 'email': 'ajdeehring@gmail.com'},
         {'id': 4221713, 'email': 'adam.deehring@gmail.com'}],
        "access": "commenter"
    }
    response = requests.get(updateSharesURL, json=badData)
    responseMessage = response.json().get("Response")
    goodMessage = 'File was not selected'
    assert responseMessage == goodMessage


def test_updateShares_BadResponse_NoRoster():
    badData = {
        "file": [{
            'id': '1hy-zLnKQ1YzRk8BEMHNgrM7kyhpvD7taXG5e6qANeZk',
            'mimeType': 'application/vnd.google-apps.presentation',
            'name': 'Teaching Tools Test Slides'
        }],
        "roster": [],
        "access": "commenter"
    }
    response = requests.get(updateSharesURL, json=badData)
    responseMessage = response.json().get("Response")
    goodMessage = 'Roster was not provided'
    assert responseMessage == goodMessage


def test_updateShares_BadResponse_NoAccess():
    badData = {
        "file": [{
            'id': '1hy-zLnKQ1YzRk8BEMHNgrM7kyhpvD7taXG5e6qANeZk',
            'mimeType': 'application/vnd.google-apps.presentation',
            'name': 'Teaching Tools Test Slides'
        }],
        "roster": [{'id': 4221108, 'email': 'ajdeehring@gmail.com'},
                   {'id': 4221713, 'email': 'adam.deehring@gmail.com'}],
        "access": ""
    }
    response = requests.get(updateSharesURL, json=badData)
    responseMessage = response.json().get("Response")
    goodMessage = 'Access option was not chosen'
    assert responseMessage == goodMessage


def test_updateShares_BadResponse_Bad1Email():
    badData = {
        "file": [{
            'id': '1hy-zLnKQ1YzRk8BEMHNgrM7kyhpvD7taXG5e6qANeZk',
            'mimeType': 'application/vnd.google-apps.presentation',
            'name': 'Teaching Tools Test Slides'
        }],
        "roster":
        [{'id': 4221108, 'email': 'ajdeehring@gmail.com'},
         {'id': 4221713, 'email': 'adam.deehring'}],
        "access": "commenter"
    }
    response = requests.get(updateSharesURL, json=badData)
    responseMessage = response.json().get("Response")
    goodMessage = 'Error: 1 email(s) failed, raised on Following ID(s): 4221713 '
    assert responseMessage == goodMessage


def test_updateShares_BadResponse_Bad2Emails():
    badData = {
        "file": [{
            'id': '1hy-zLnKQ1YzRk8BEMHNgrM7kyhpvD7taXG5e6qANeZk',
            'mimeType': 'application/vnd.google-apps.presentation',
            'name': 'Teaching Tools Test Slides'
        }],
        "roster":
        [{'id': 4221108, 'email': 'ajdeehring'},
         {'id': 4221713, 'email': 'adam.deehring'}],
        "access": "commenter"
    }
    response = requests.get(updateSharesURL, json=badData)
    responseMessage = response.json().get("Response")
    goodMessage = 'Error: 2 email(s) failed, raised on Following ID(s): 4221108 4221713 '
    assert responseMessage == goodMessage
