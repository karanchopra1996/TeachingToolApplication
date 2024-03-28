import requests


URL = "http://127.0.0.1:5000/settings"

#-----------------------------------------------------------------------------------------------   
#A correct case
def test_good(): 
    data = {
    "courseId":"1521081",
    "importCourse":"1521081"
    }   
    response = requests.post(URL, json = data) 
    assert response.json().get('status_code') == 200

#----------------------------------------------------------------------------------------------- 
#Incorrect course id
def test_bad1(): 
    data = {
    "courseId":"a",
    "importCourse":"Teaching Tools Testbed"
    }   
    response = requests.post(URL, json = data)
    assert response.json().get('status_code') == 500

#-----------------------------------------------------------------------------------------------
#Incorrect importCourse id
def test_bad2(): 
    data = {
    "courseId":"Teaching Tools Testbed",
    "importCourse":"a"
    }   
    response = requests.post(URL, json = data)
    assert response.json().get('status_code') == 500
     
#-----------------------------------------------------------------------------------------------
#Both incorrect courseId and importCourse
def test_bad3(): 
    data = {
    "courseId":"a",
    "importCourse":"a"
    }   
    response = requests.post(URL, json = data)
    assert response.json().get('status_code') == 500


#-----------------------------------------------------------------------------------------------
#Incorrect courseId key
def test_bad4(): 
    data = {
    "a":"a",
    "importCourse":"a"
    }   
    response = requests.post(URL, json = data)
    assert response.json().get('status_code') == 500

#-----------------------------------------------------------------------------------------------
#Incorrect importCourse key
def test_bad5(): 
    data = {
    "courseId":"a",
    "a":"a"
    }   
    response = requests.post(URL, json = data)
    assert response.json().get('status_code') == 500
