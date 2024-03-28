"""Pytest cases for Functions file googleFile.py"""

import requests

fromDriveURL = "http://127.0.0.1:5000/downloadGoogleFile"
fromDriveGoodData_pptx = {
    "courseID": "1521081",
    "file": [{
        'id': '17mC3lYAWlkt6BVNLeMvxEer81HEmapFI',
        'mimeType': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
        'name': 'Azure DevOps Overview and Engineering Process Primer.pptx'
    }],
    "destFolder": "course files/Folder 1/Testing Folder 2"
}

fromDriveGoodData_jpg = {
    "courseID": "1521081",
    "file": [{
        'id': '1YPRh-KcEvgvZ1TW9VR5lwfaxfk4tV68h',
        'mimeType': 'image/jep',
        'name': 'wn-campus-aerial.jpg'
    }],
    "destFolder": "course files/Folder 1/Testing Folder 2"
}

fromDriveGoodData_png = {
    "courseID": "1521081",
    "file": [{
        'id': '15swiKbW45UvmAs4aYQktgx14mbLR1xtL',
        'mimeType': 'image/png',
        'name': 'UW-Logo.png'
    }],
    "destFolder": "course files/Folder 1/Testing Folder 2"
}

fromDriveGoodData_xlsx = {
    "courseID": "1521081",
    "file": [{
        'id': '1x83VTjaGgisRkXkTfRZVXe3JKkCAoQkQ',
        'mimeType': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'name': 'Large Dataset.xlsx',
    }],
    "destFolder": "course files/Folder 1/Testing Folder 2"
}

fromDriveGoodData_pdf = {
    "courseID": "1521081",
    "file": [{
        'id': '0BxEDq9lfdR3Xc3RhcnRlcl9maWxlX2Rhc2hlclYw',
        'mimeType': 'application/pdf',
        'name': 'Getting started',
    }],
    "destFolder": "course files/Folder 1/Testing Folder 2"
}

fromDriveGoodData_multipleFiles = {
    "courseID": "1521081",
    "file": [{
        'id': '1APms7JFUZtMwCdorJ4O-NNh5z4hb7Z_w',
        'mimeType': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
        'name': 'PPT_Template_16x9-Gradient-ADA.pptx'
    }, {
        'id': '17Joo9eWlw4hzv7etp-XiCt57kt30dfX6',
        'mimeType': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'name': 'StyledWordDoc-Photo-ADA.docx',
    }],
    "destFolder": "course files/Folder 1/Testing Folder 2"
}


def test_fromGoogleDrive_Good():
    response = requests.get(fromDriveURL, json=fromDriveGoodData_pptx)
    assert response.status_code == 200


def test_fromGoogleDrive_Bad():
    badURL = "http://127.0.0.1:5000/downloadGoogle"
    response = requests.get(badURL, json=fromDriveGoodData_pptx)
    assert response.status_code == 404


def test_fromGoogleDrive_GoodResponse_pptx():
    response = requests.get(fromDriveURL, json=fromDriveGoodData_pptx)
    responseMessage = response.json().get("Response")
    goodMessage = 'Successfully Uploaded All Files to Target Destination: 1 file(s) successfully uploaded '
    assert responseMessage == goodMessage


def test_fromGoogleDrive_GoodResponse_jpeg():
    response = requests.get(fromDriveURL, json=fromDriveGoodData_jpg)
    responseMessage = response.json().get("Response")
    goodMessage = 'Successfully Uploaded All Files to Target Destination: 1 file(s) successfully uploaded '
    assert responseMessage == goodMessage


def test_fromGoogleDrive_GoodResponse_pdf():
    response = requests.get(fromDriveURL, json=fromDriveGoodData_pdf)
    responseMessage = response.json().get("Response")
    goodMessage = 'Successfully Uploaded All Files to Target Destination: 1 file(s) successfully uploaded '
    assert responseMessage == goodMessage


def test_fromGoogleDrive_GoodResponse_png():
    response = requests.get(fromDriveURL, json=fromDriveGoodData_png)
    responseMessage = response.json().get("Response")
    goodMessage = 'Successfully Uploaded All Files to Target Destination: 1 file(s) successfully uploaded '
    assert responseMessage == goodMessage


def test_fromGoogleDrive_GoodResponse_xlsx():
    response = requests.get(fromDriveURL, json=fromDriveGoodData_xlsx)
    responseMessage = response.json().get("Response")
    goodMessage = 'Successfully Uploaded All Files to Target Destination: 1 file(s) successfully uploaded '
    assert responseMessage == goodMessage


def test_fromGoogleDrive_GoodResponse_multipleFiles():
    response = requests.get(fromDriveURL, json=fromDriveGoodData_multipleFiles)
    responseMessage = response.json().get("Response")
    goodMessage = 'Successfully Uploaded All Files to Target Destination: 2 file(s) successfully uploaded '
    assert responseMessage == goodMessage


def test_fromGoogleDrive_BadFolderResponse():
    badData = {
        "courseID": "1521081",
        "file": [{
            'id': '17mC3lYAWlkt6BVNLeMvxEer81HEmapFI',
            'mimeType': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
            'name': 'Azure DevOps Overview and Engineering Process Primer.pptx'
        }],
        "destFolder": "course files/Folder 1/This Folder Does Not Exist"
    }
    response = requests.get(fromDriveURL, json=badData)
    responseMessage = response.json().get("Response")
    goodMessage = 'Folder was Not Found'
    assert responseMessage == goodMessage


def test_fromGoogleDrive_BadCourseResponse():
    badData = {
        "courseID": "1521080871",
        "file": [{
            'id': '17mC3lYAWlkt6BVNLeMvxEer81HEmapFI',
            'mimeType': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
            'name': 'Azure DevOps Overview and Engineering Process Primer.pptx'
        }],
        "destFolder": "course files/Folder 1/Testing Folder 2"
    }
    response = requests.get(fromDriveURL, json=badData)
    responseMessage = response.json().get("Response")
    goodMessage = 'Course was Not Found'
    assert responseMessage == goodMessage
