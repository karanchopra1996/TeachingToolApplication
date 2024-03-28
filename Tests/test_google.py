"""Pytest cases for Functions file uploadGoogleFile.py"""

import requests
URL = "http://127.0.0.1:5000/getGoogDoc"
goodData = {
    "docID" : "1lL7ySV7CNhUNcn8WthR3lU5qoJ0nJN0KPgDnVZOb8Tw",
    "docName": "Testing Pages_14",
    "type" : "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "courseID" : "1521081",
    "folder" : "course files"
}
#-----------------------------------------------------------------------------------
#Test cases for uploadToCanvasManager function
def test_statusCode_Good():
    response = requests.get(URL, json = goodData)
    assert response.status_code == 200

def test_statusCode_Bad():
    badURL = "http://127.0.0.1:5000/getGoogleDoc"
    response = requests.get(badURL, json = goodData)
    assert response.status_code == 404

def test_goodResponse():
    response = requests.get(URL, json = goodData)
    responseMessage = response.json().get('Response')
    goodMessage = 'Successfully imported file to the course.'
    assert responseMessage == goodMessage

def test_badResponse():
    badData = {
        "docID" : "1Qcj-Gset7ZCZ1D-3ZVnZXGnC4lgU2PXwbJC",
        "docName": "Testing Pages_14",
        "type" : "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "courseID" : "15210312321",
        "folder" : "course files"
    }
    response = requests.get(URL, json = badData)
    responseMessage = response.json().get('Response')
    goodMessage = 'There was an error finding the google file.'
    assert responseMessage == goodMessage