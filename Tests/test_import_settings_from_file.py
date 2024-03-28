import requests

URL = "http://127.0.0.1:5000/settingsFromFiles"

#-----------------------------------------------------------------------------------------------
# tests adding members to groups, creating new group categories, and creating new groups
def test_good():
    files = {'navFile': open('Tests/fileGood-Navigation.json', 'rb'),
            'settingsFile': open('Tests/fileGood-Settings.json', 'rb')}
    data = {"courseId":"1521081"}

    response = requests.post(URL, files=files, data=data) 
    assert response.json().get('status_code') == 200 
    assert response.json().get('message') == "Imported settings and navigation to course."

#-----------------------------------------------------------------------------------------------
# tests incorrect naming for data key
def test_bad1():
    files = {'navFile': open('Tests/fileGood-Navigation.json', 'rb'),
            'settingsFile': open('Tests/fileGood-Settings.json', 'rb')}
    data = {"course":"1521081"}
    response = requests.post(URL, files=files, data=data) 
    assert response.json().get('status_code') == 500
    assert response.json().get('message') == "KeyError or Course Doesnt exist"

#-----------------------------------------------------------------------------------------------
# tests incorrect naming for nav file key
def test_bad2():
    files = {'nav': open('Tests/fileGood-Navigation.json', 'rb'),
            'settingsFile': open('Tests/fileGood-Settings.json', 'rb')}
    data = {"courseId":"1521081"}
    response = requests.post(URL, files=files, data=data) 
    assert response.json().get('status_code') == 500
    assert response.json().get('message') == "KeyError or Course Doesnt exist"

#-----------------------------------------------------------------------------------------------
# tests incorrect naming for settings file key
def test_bad3():
    files = {'navFile': open('Tests/fileGood-Navigation.json', 'rb'),
            'settings': open('Tests/fileGood-Settings.json', 'rb')}
    data = {"courseId":"1521081"}

    response = requests.post(URL, files=files, data=data) 
    assert response.json().get('status_code') == 500 
    assert response.json().get('message') == "KeyError or Course Doesnt exist"

#-----------------------------------------------------------------------------------------------
# tests incorrect courseId
def test_bad4():
    files = {'navFile': open('Tests/fileGood-Navigation.json', 'rb'),
            'settingsFile': open('Tests/fileGood-Settings.json', 'rb')}
    data = {"courseId":"a"}
    response = requests.post(URL, files=files, data=data) 
    assert response.json().get('status_code') == 500
    assert response.json().get('message') == "KeyError or Course Doesnt exist"

#-----------------------------------------------------------------------------------------------
# test incorect key in nav json file
def test_bad5():
    files = {'navFile': open('Tests/fileBadKey-Navigation.json', 'rb'),
            'settingsFile': open('Tests/fileGood-Settings.json', 'rb')}
    data = {"courseId":"1521081"}
    response = requests.post(URL, files=files, data=data) 
    assert response.json().get('status_code') == 500
    assert response.json().get('message') == "Failed to import settings or navigation"

#-----------------------------------------------------------------------------------------------
# test incorect value in nav json file
def test_bad6():
    files = {'navFile': open('Tests/fileBadValue-Navigation.json', 'rb'),
            'settingsFile': open('Tests/fileGood-Settings.json', 'rb')}
    data = {"courseId":"1521081"}
    response = requests.post(URL, files=files, data=data) 
    assert response.json().get('status_code') == 500
    assert response.json().get('message') == "Failed to import settings or navigation"
