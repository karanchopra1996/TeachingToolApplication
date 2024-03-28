"""Pytest cases for Functions file canvasSyllabus.py"""

import requests

URL = "http://127.0.0.1:5000/getSyllabus"
goodData = {
    "courseID": "1521081",
    "toLocal": False
}
#----------------------------------------------------------------------------
#Tests for downloadSyllabus function
def test_statusCode_Good():
    response = requests.get(URL, json=goodData)
    assert response.status_code == 200

def test_statusCode_Bad():
    badURL = "http://127.0.0.1:5000/getSlly"
    response = requests.get(badURL, json=goodData)
    assert response.status_code == 404

def test_goodResponse():
    response = requests.get(URL, json=goodData)
    responseMessage = response.json().get('Response')
    goodMessage = 'Uploaded Syllabus file to Google Drive.'
    assert responseMessage == goodMessage

def test_badResponse():
    badData = {
        "courseID": "1283192312",
        "toLocal": False
    }
    response = requests.get(URL, json=badData)
    responseMessage = response.json().get('Response')
    goodMessage = "There was an error finding the course."
    assert responseMessage == goodMessage
