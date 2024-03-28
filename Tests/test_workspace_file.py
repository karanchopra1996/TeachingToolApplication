"""Pytest cases for Functions file googleFile.py"""

import requests

fromDriveURL = "http://127.0.0.1:5000/downloadWorkspaceFile"
""""""
fromDriveGoodData_slides = {
    "courseID": "1521081",
    "file": [{
        'id': '1hy-zLnKQ1YzRk8BEMHNgrM7kyhpvD7taXG5e6qANeZk',
        'mimeType': 'application/vnd.google-apps.presentation',
        'name': 'Teaching Tools Test Slides'
    }],
    "destFolder": "course files/Folder 1/Testing Folder 2"
}
fromDriveGoodData_sheets = {
    "courseID": "1521081",
    "file": [{
        'id': '1cdjz7A_37RjiIH_bzOMmwawsURautxyGaVt7UEHoWJ8',
        'mimeType': 'application/vnd.google-apps.spreadsheet',
        'name': 'Teaching Tools Testbed Assignments'
    }],
    "destFolder": "course files/Folder 1/Testing Folder 2"
}
fromDriveGoodData_docs = {
    "courseID": "1521081",
    "file": [{
        'id': '1rZnj5HG1bEtFTII2sWb1At7IsSBJTBcrCWxQ5oxCqL4',
        'mimeType': 'application/vnd.google-apps.document',
        'name': 'Teaching Tools Testbed_TTT_Syllabus'
    }],
    "destFolder": "course files/Folder 1/Testing Folder 2"
}
fromDriveGoodData_docs2 = {
    "courseID": "1521081",
    "file": [{
        'id': '1lL7ySV7CNhUNcn8WthR3lU5qoJ0nJN0KPgDnVZOb8Tw',
        'mimeType': 'application/vnd.google-apps.document',
        'name': 'Testing Pages-14'
    }],
    "destFolder": "course files/Folder 1/Testing Folder 2"
}


def test_fromGoogleDrive_Good():
    response = requests.get(fromDriveURL, json=fromDriveGoodData_docs2)
    assert response.status_code == 200


def test_fromGoogleDrive_Bad():
    badURL = "http://127.0.0.1:5000/exportWorkspace"
    response = requests.get(badURL, json=fromDriveGoodData_docs2)
    assert response.status_code == 404


def test_fromGoogleDrive_GoodResponse_pptx():
    response = requests.get(fromDriveURL, json=fromDriveGoodData_slides)
    responseMessage = response.json().get("Response")
    goodMessage = 'Successfully Uploaded All Files to Target Destination: 1 file(s) successfully uploaded '
    assert responseMessage == goodMessage


def test_fromGoogleDrive_GoodResponse_xlxs():
    response = requests.get(fromDriveURL, json=fromDriveGoodData_sheets)
    responseMessage = response.json().get("Response")
    goodMessage = 'Successfully Uploaded All Files to Target Destination: 1 file(s) successfully uploaded '
    assert responseMessage == goodMessage


def test_fromGoogleDrive_GoodResponse_docs():
    response = requests.get(fromDriveURL, json=fromDriveGoodData_docs)
    responseMessage = response.json().get("Response")
    goodMessage = 'Successfully Uploaded All Files to Target Destination: 1 file(s) successfully uploaded '
    assert responseMessage == goodMessage


def test_fromGoogleDrive_BadFolderResponse():
    badData = {
        "courseID": "1521081",
        "file": [{
            'id': '1rZnj5HG1bEtFTII2sWb1At7IsSBJTBcrCWxQ5oxCqL4',
            'mimeType': 'application/vnd.google-apps.document',
            'name': 'Teaching Tools Testbed_TTT_Syllabus'
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
            'id': '1rZnj5HG1bEtFTII2sWb1At7IsSBJTBcrCWxQ5oxCqL4',
            'mimeType': 'application/vnd.google-apps.document',
            'name': 'Teaching Tools Testbed_TTT_Syllabus'
        }],
        "destFolder": "course files/Folder 1/Testing Folder 2"
    }
    response = requests.get(fromDriveURL, json=badData)
    responseMessage = response.json().get("Response")
    goodMessage = 'Course was Not Found'
    assert responseMessage == goodMessage
