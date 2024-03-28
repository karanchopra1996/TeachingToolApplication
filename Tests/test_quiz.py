"""PyTest cases for Functions file canvasQuizzes.py"""

import requests

quizzesURL = "http://127.0.0.1:5000/exportQuizzes"
quizGoodData = {
    "courseID": "1521081"
}
submissionsURL = "http://127.0.0.1:5000/downloadQuizSubmissions"
submissionGoodData = {
    "courseID": "1521081",
    "Quiz_ID" : "1617705"
}
#---------------------------------------------------------------------
#Test cases for downloadQuizzes function
def test_Quiz_statusCode_Good():
    response = requests.get(quizzesURL, json=quizGoodData)
    assert response.status_code == 200

def test_Quiz_statusCode_Bad():
    badURL = "http://127.0.0.1:5000/importQuiz"
    response = requests.get(badURL, json=quizGoodData)
    assert response.status_code == 404

def test_Quiz_goodResponse():
    response = requests.get(quizzesURL, json=quizGoodData)
    responseMessage = response.json().get('Response')
    goodMessage = 'Successfully downloaded quizzes.'
    assert responseMessage == goodMessage

def test_Quiz_badResponse():
    badData = {
        "courseID": "1519021"
    }
    response = requests.get(quizzesURL, json=badData)
    # responseMessage = response.json().get('Response')
    # goodMessage = 'There was an error downloading the quizzes.'
    # assert responseMessage == goodMessage
    assert response.status_code == 500
    
#---------------------------------------------------------------------
#Test cases for exportQuizSubmissions function
def test_Submission_statusCode_Good():
    response = requests.get(submissionsURL, json=submissionGoodData)
    assert response.status_code == 200

def test_Submission_statusCode_Bad():
    badURL = "http://127.0.0.1:5000/downloadQuizSubmissssions"
    response = requests.get(badURL, json=submissionGoodData)
    assert response.status_code == 404

def test_Submission_goodResponse():
    response = requests.get(submissionsURL, json=submissionGoodData)
    responseMessage = response.json().get('Response')
    goodMessage = 'Successfully downloaded all submissions for quiz: Quiz 1'
    assert responseMessage == goodMessage

def test_Submission_badResponse():
    badData = {
        "courseID": "1519021",
        "Quiz_ID" : "12314141"
    }
    response = requests.get(submissionsURL, json=badData)
    # responseMessage = response.json().get('Response')
    # goodMessage = 'Error retrieving Quiz submissions.'
    # assert responseMessage == goodMessage
    assert response.status_code == 500