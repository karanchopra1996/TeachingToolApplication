"""Pytest cases for Functions file googleFile.py"""

import requests

toCanvasURL = "http://127.0.0.1:5000/createCanvasFolder"
deleteCanvasURL = "http://127.0.0.1:5000/deleteCanvasFolder"
toCanvasGoodData = {
    'courseID': '1521081',
    'folderName': 'This Folder is for a Unit Test',
    'parentFolder': 'course files/Folder 1'
}

toDriveURL = "http://127.0.0.1:5000/createGoogleFolder"
deleteDriveURL = "http://127.0.0.1:5000/deleteGoogleFolder"
toDriveGoodData = {
    'courseID': '1521081',
    'folderName': 'This Folder is for a Unit Test',
    "parentFolder": [{
        'id': '1u59M_t9FrX2MuiXO294z9bnfjZeiVOXZ',
    }]
}


def test_toCanvas_Good():
    response1 = requests.get(toCanvasURL, json=toCanvasGoodData)
    assert response1.status_code == 200
    folderID = response1.json().get('Folder').get('id')
    response = requests.get(deleteCanvasURL, json={'folderID': folderID})
    assert response.status_code == 200


def test_toCanvas_Bad():
    badURL = "http://127.0.0.1:5000/createFolder"
    response = requests.get(badURL, json=toCanvasGoodData)
    assert response.status_code == 404


def test_toCanvas_GoodResponse():
    response = requests.get(toCanvasURL, json=toCanvasGoodData)
    responseMessage = response.json().get('Response')
    goodMessage = "Folder 'This Folder is for a Unit Test' created"
    assert goodMessage == responseMessage
    folderID = response.json().get('Folder').get('id')
    response = requests.get(deleteCanvasURL, json={'folderID': folderID})
    responseMessage = response.json().get('Response')
    goodMessage = "Success"
    assert goodMessage == responseMessage


def test_toCanvas_BadCourse():
    badData = {
        "courseID": "1527981081",
        'folderName': 'New Folder',
        'parentFolder': 'course files/Folder 1'
    }
    response = requests.get(toCanvasURL, json=badData)
    responseMessage = response.json().get('Response')
    goodMessage = "Course was Not Found"
    assert goodMessage == responseMessage


def test_toCanvas_BadFolderLocation():
    badData = {
        "courseID": "1521081",
        'folderName': 'Folder 1',
        'parentFolder': 'course flies'
    }
    response = requests.get(toCanvasURL, json=badData)
    responseMessage = response.json().get('Response')
    goodMessage = "Folder was Not Found"
    assert goodMessage == responseMessage


def test_toCanvas_BadFolderName():
    badData = {
        "courseID": "1521081",
        'folderName': 'Folder 1',
        'parentFolder': 'course files'
    }
    response = requests.get(toCanvasURL, json=badData)
    responseMessage = response.json().get('Response')
    goodMessage = "Folder already exist with this context"
    assert goodMessage == responseMessage


def test_toDrive_Good():
    response = requests.get(toDriveURL, json=toDriveGoodData)
    assert response.status_code == 200
    response = requests.get(deleteDriveURL, json={
                            'folderID': response.json().get('Folder').get('id')})
    assert response.status_code == 200


def test_toDrive_Bad():
    badURL = "http://127.0.0.1:5000/createFolder"
    response = requests.get(badURL, json=toDriveGoodData)
    assert response.status_code == 404


def test_toDrive_GoodResponse():
    response = requests.get(toDriveURL, json=toDriveGoodData)
    responseMessage = response.json().get('Response')
    goodMessage = "Folder 'This Folder is for a Unit Test' created"
    assert goodMessage == responseMessage
    response = requests.get(deleteDriveURL, json={
                            'folderID': response.json().get('Folder').get('id')})
    responseMessage = response.json().get('Response')
    goodMessage = "Success"
    assert goodMessage == responseMessage


def test_toDrive_BadFolderLocation():
    badData = {
        "courseID": "1521081",
        'folderName': 'Folder 1',
        "parentFolder": [{
            'id': '',
        }]
    }
    response = requests.get(toDriveURL, json=badData)
    responseMessage = response.json().get('Response')
    goodMessage = "Error: Folder was not Created"
    assert goodMessage == responseMessage
