import requests


URL = "http://127.0.0.1:5000/exportSettings"

#-----------------------------------------------------------------------------------------------   
#A correct case
def test_good(): 
    data = {
    "courseId":"1521081"
    }   
    response = requests.post(URL, json = data) 
    assert response.status_code == 200

#----------------------------------------------------------------------------------------------- 
#Incorrect course id
def test_bad1(): 
    data = {
    "courseId":"a"
    }   
    response = requests.post(URL, json = data)
    assert response.status_code == 500

#-----------------------------------------------------------------------------------------------
#Incorrect course id
def test_bad2(): 
    data = {
    "courseId":"1"
    }   
    response = requests.post(URL, json = data)
    assert response.status_code == 500

#-----------------------------------------------------------------------------------------------
#Incorrect course id
def test_bad3(): 
    data = {
    "courseId":1
    }   
    response = requests.post(URL, json = data)
    assert response.status_code == 500
 
#-----------------------------------------------------------------------------------------------
#Incorrect course id key
def test_bad4(): 
    data = {
    "course":1
    }   
    response = requests.post(URL, json = data)
    assert response.status_code == 500
