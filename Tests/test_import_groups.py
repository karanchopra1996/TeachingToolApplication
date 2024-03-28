import requests

URL = "http://127.0.0.1:5000/importStudentGroups"

#-----------------------------------------------------------------------------------------------
# tests adding members to groups, creating new group categories, and creating new groups
def test_good():
    groupsFile = {'file': open('Tests/fileNoGroups.csv', 'rb')}
    data = {"courseId":"1521081"}
    response = requests.post(URL, files=groupsFile, data=data) 
    assert response.json().get('status_code') == 200 
    assert response.json().get('message') == "Groups created"
    
#-----------------------------------------------------------------------------------------------
# tests incorrect naming for json data key
def test_bad1():
    groupsFile = {'file': open('Tests/fileNoGroups.csv', 'rb')}
    data = {"course":"1521081"}
    response = requests.post(URL, files=groupsFile, data=data) 
    assert response.json().get('status_code') == 500
    assert response.json().get('message') == "KeyError or Course Doesnt exist"

#-----------------------------------------------------------------------------------------------
# tests incorrect naming for file key
def test_bad2():
    groupsFile = {'files': open('Tests/fileNoGroups.csv', 'rb')}
    data = {"courseId":"1521081"}
    response = requests.post(URL, files=groupsFile, data=data) 
    assert response.json().get('status_code') == 500
    assert response.json().get('message') == "KeyError or Course Doesnt exist"

#-----------------------------------------------------------------------------------------------
# tests incorrect courseId
def test_bad3():
    groupsFile = {'file': open('Tests/fileNoGroups.csv', 'rb')}
    data = {"courseId":"a"}
    response = requests.post(URL, files=groupsFile, data=data) 
    assert response.json().get('status_code') == 500
    assert response.json().get('message') == "KeyError or Course Doesnt exist"
    
#-----------------------------------------------------------------------------------------------
# tests incorrect headers
def test_bad4():
    groupsFile = {'file': open('Tests/fileWrongHeaders.csv', 'rb')}
    data = {"courseId":"1521081"}
    response = requests.post(URL, files=groupsFile, data=data) 
    assert response.json().get('status_code') == 500
    assert response.json().get('message') == "Incorrect header naming"
