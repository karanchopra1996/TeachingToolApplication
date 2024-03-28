"""Pytest cases for Functions file canvasPages.py"""

import requests

toDriveURL = "http://127.0.0.1:5000/getPageInfoToDrive"
toCanvasURL = "http://127.0.0.1:5000/getDriveFileToCanvas" 
toDriveGoodData = {
    "courseID": "1521081",
    "Canvas_Page": "Testing Pages"}
toCanvasGoodData = {
    "courseID": "1521081",
    "Google_FileID" : "1lL7ySV7CNhUNcn8WthR3lU5qoJ0nJN0KPgDnVZOb8Tw",
    "Google_File": "Testing Pages_14"}


#-----------------------------------------------------------------------------
# Test cases for downloadPageToDrive function

def test_toGoogleStatusCode_Good():
    response = requests.get(toDriveURL, json=toDriveGoodData)
    assert response.status_code == 200

def test_toGoogleStatusCode_Bad():
    badURL = "http://127.0.0.1:5000/getPageInfo"
    response = requests.get(badURL, json=toDriveGoodData)
    assert response.status_code == 404

def test_toGoogleGoodResponse():
    response = requests.get(toDriveURL, json=toDriveGoodData)
    responseMessage = response.json().get('Response')
    goodMessage = 'Successfully exported canvas page and imported it to google drive'
    assert responseMessage == goodMessage

def test_toGoogleBadResponse():
    badData = {
        "courseID": "187984652",
        "Canvas_Page": "Nonexistent Page"
    }
    response = requests.get(toDriveURL, json=badData)
    responseMessage = response.json().get('Response')
    goodMessage = 'There was an error finding the course.'
    assert responseMessage == goodMessage

   #--------------------------------------------------------------------------------------
   # Test cases for downloadFromDriveToCanvasPage function
def test_toCanvasStatusCode_Good():
    response = requests.get(toCanvasURL, json=toCanvasGoodData)
    assert response.status_code == 200

def test_toCanvasStatusCode_Bad():
    badURL = "http://127.0.0.1:5000/getPageInfo"
    response = requests.get(badURL, json=toCanvasGoodData)
    assert response.status_code == 404

def test_toCanvasGoodResponse():
    response = requests.get(toCanvasURL, json=toCanvasGoodData)
    responseMessage = response.json().get('Response')
    goodMessage = 'Successfully created canvas page from google drive file'
    assert responseMessage == goodMessage

def test_toCanvasBadResponse():
    badData = {
        "courseID": "1521081",
        "Google_FileID" : "1of9D080989CMihFM5iSWGXSQLVyDZe4mZIbkW2s-_r0-lQ",
        "Google_File": "This is a Test_13"
    }
    response = requests.get(toCanvasURL, json=badData)
    responseMessage = response.json().get('Response')
    goodMessage = 'There was an error finding the google file.'
    assert responseMessage == goodMessage
