from os import stat
import lxml.etree as etree
import os
from types import resolve_bases
from flask_cors import CORS
from dotenv import load_dotenv
import json
from flask_swagger_ui import get_swaggerui_blueprint
from flask import Flask, jsonify, session as flask_session
from flask import request
from logging.config import dictConfig
import ssl
from core.canvas_services import canvas_services as canvasCore
from core.google_services import google_services as googleCore
from flask import Flask, request, jsonify

from google import googleFunctions
from google import googleFile
from google import googleWorkspaceFile

import datetime
import pytz
import secrets
from flask_session import Session
import requests
import ssl
from flask import Flask


from datetime import timedelta

load_dotenv()

# Canvas API URL
canvas_base_url = "https://canvas.uw.edu/api/v1/"

app = Flask(__name__)


app.config["SESSION_TYPE"] = "filesystem"  # Use server-side sessions
app.config["SECRET_KEY"] = "12345"
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=2)
Session(app)
# Initialize sessions

# -----------------SWAGGER CONFIGURATIONS------------------------------------------------------------------------------
swagger_url = "/swagger"
swagger_api_url = "/static/swagger.json"
swagger_blue_print = get_swaggerui_blueprint(
    swagger_url,
    swagger_api_url,
    config={"app_name": " Teaching Tools - Software Engineering Studio"},
)
app.register_blueprint(swagger_blue_print, url_prefix=swagger_url)

CORS(app)


def get_canvas_instance():
    login_method = os.getenv("LOGIN_METHOD")

    if login_method == "TOKEN":
        access_token = os.getenv("CANVAS_ACCESS_TOKEN")
        flask_session["access_token"] = access_token
    else:
        print(f"Using OAuth login method")
    if "access_token" in flask_session:
        access_token = flask_session["access_token"]
        canvas_headers = {"Authorization": "Bearer " + access_token}
        return canvasCore(canvas_base_url, canvas_headers)
    else:
        print("No access token found in session.")
        return None


# -----------------------------------------------------------------------------------------------
@app.route("/")
def hello_world():
    app.logger.info("A user visited the home page")
    login_method = os.getenv("LOGIN_METHOD")
    if login_method == "OAUTH":
        # Render a login button for OAuth method
        return "Please login using OAuth"  # You can provide HTML templates for a login button here
    else:
        # Continue with your app logic
        app.logger.info(os.getenv("LOGIN_METHOD"))
        return {"Selene": "Selene"}


# -----------------------------------Canvas OAuth 2.0 Routes------------------------------------------------------------

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


@app.route("/api/get-client-id", methods=["GET"])
def get_client_id():
    return jsonify({"client_id": client_id})


@app.route("/api/clear_session", methods=["POST"])
def clear_session_endpoint():
    print("Received request to clear the current user session.")
    flask_session.pop("access_token", None)
    flask_session.pop("refresh_token", None)
    flask_session.pop("token_expiry", None)
    return jsonify({"message": "Session cleared successfully"}), 200


@app.route("/api/authorization-code", methods=["POST"])
def receive_authorization_code():
    data = request.get_json()
    code = data.get("code")
    current_url = data.get("currentUrl")
    try:
        exchange_code_for_token(code, current_url)
        flask_session["current_url"] = current_url
        return jsonify({"status": "200"})
    except:
        return jsonify({"status": "400"})


def save_access_token_info(access_token_response):
    flask_session["access_token"] = access_token_response["access_token"]
    flask_session["refresh_token"] = access_token_response["refresh_token"]
    expiry_time = datetime.datetime.now(pytz.utc) + datetime.timedelta(
        seconds=access_token_response["expires_in"]
    )
    flask_session["token_expiry"] = expiry_time.isoformat()


def exchange_code_for_token(code, current_url):
    scopes = [
        "url:GET|/api/v1/courses",
        "url:GET|/api/v1/users/:user_id/courses",
        "url:GET|/api/v1/courses/:course_id/groups",
        "url:GET|/api/v1/courses/:course_id/settings",
        "url:GET|/api/v1/group_categories/:group_category_id",
        "url:GET|/api/v1/courses/:course_id/search_users",
        "url:GET|/api/v1/groups/:group_id",
        "url:GET|/api/v1/courses/:course_id/group_categories",
        "url:GET|/api/v1/group_categories/:group_category_id/groups",
    ]

    token_url = "https://canvas.uw.edu/login/oauth2/token"
    data = {
        "code": code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": "https://localhost:3000",
        "grant_type": "authorization_code",
    }
    response = requests.post(token_url, data=data)
    response.raise_for_status()
    if response.status_code == 200:
        access_token_response = response.json()
        flask_session.clear()
        save_access_token_info(access_token_response)
    else:
        print(f"Error exchanging code for token: {response.text}")
    return response.status_code


@app.route("/api/check-login", methods=["GET"])
def check_login():
    access_token = flask_session.get("access_token")
    if access_token is None or access_token == "":
        return jsonify({"isLoggedIn": False}), 401

    token_expiry_str = flask_session.get("token_expiry")
    token_expiry = datetime.datetime.fromisoformat(token_expiry_str)
    current_time = datetime.datetime.now(pytz.utc)

    if token_expiry is None or (token_expiry - current_time).total_seconds() < 0:
        refresh_token = flask_session.get("refresh_token")
        if refresh_token is None:
            flask_session.pop("access_token", None)
            flask_session.pop("refresh_token", None)
            flask_session.pop("token_expiry", None)
            print("No refresh token found. Access token has expired.")
            return jsonify({"isLoggedIn": False}), 401
        else:
            access_token_response = refresh_access_token(refresh_token)
            if access_token_response is None:
                flask_session.pop("access_token", None)
                flask_session.pop("refresh_token", None)
                flask_session.pop("token_expiry", None)
                print("Error refreshing access token.")
                return jsonify({"isLoggedIn": False}), 401
            else:
                save_access_token_info(access_token_response)
                print(f"isLoggedIn will be true")
                return jsonify({"isLoggedIn": True})
    else:
        return jsonify({"isLoggedIn": True})


def refresh_access_token(refresh_token):
    token_url = "https://canvas.uw.edu/login/oauth2/token"
    data = {
        "refresh_token": refresh_token,
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "refresh_token",
    }
    response = requests.post(token_url, data=data)

    if response.status_code == 200:
        access_token_response = response.json()
        save_access_token_info(access_token_response)
        return access_token_response
    else:
        print("Error refreshing access token:", response.text)
        return None


@app.route("/api/access_token", methods=["DELETE"])
def delete_access_token():
    try:
        flask_session.pop("access_token", None)
        flask_session.pop("token_type", None)
        flask_session.pop("token_expiry", None)
        flask_session.pop("current_url", None)
        return "", 204
    except:
        return "Error occured while deleting access token", 500


# Initialize a new canvas_services object
# canvas = canvasCore(canvas_base_url, canvas_headers)


# -----------------------------------Google App Routes------------------------------------------------------------
# Returns a list of all the user's Google Drive Files
@app.route("/getGoogleFiles", methods=["POST", "GET"])
def getGoogleFiles():
    """Returns a list of all the user's Google Drive Files"""
    # fileList = Functions.googleFunctions.getGoogleDriveFiles()
    # files = []
    # x = 0
    # for file in fileList:
    #     if file.get('mimeType') == 'application/vnd.google-apps.document':
    #         entry = {'id': file.get('id'), 'title': (
    #             file.get('name') + "_" + str(x)), 'type': file.get('mimeType')}
    #         files.append(entry)
    #         x = x + 1
    files = googleFunctions.getFilesList()
    return jsonify(files=files)


# Imports file from Google Drive and exports it to a specific course folder
@app.route("/getGoogDoc", methods=["GET", "POST"])
def getGoogDoc():
    """Imports file from Google Drive and exports it to a specific course folder"""
    response = request.get_json(force=True)
    docID = response["docID"]
    docName = response["docName"]
    type = response["type"]
    courseID = response["courseID"]
    folder = response["folder"]
    # status = Functions.uploadGoogleFile.uploadToCanvasManager(
    #     courseID, docID, docName, type, folder)

    fileName = googleFunctions.downloadFile(docID, docName, type)
    if fileName == "Error":
        return {"Response": "There was an error retrieving the google file."}
    canvas = get_canvas_instance()
    if canvas is None:
        return jsonify({"error": "Not authenticated"}), 401
    canvas.uploadFile(courseID, fileName, parent_folder_path=folder)
    return {"Response": "Successfully imported file to the course."}


# Exports a Canvas Page contents to a Google Drive File
@app.route("/getPageInfoToDrive", methods=["GET", "POST"])
def downloadPageInfoToDrive():
    """Exports a Canvas Page to a Google Drive File"""
    response = request.get_json(force=True)
    courseID = response["courseID"]
    canvasPage = response["Canvas_Page"]
    canvas = get_canvas_instance()
    if canvas is None:
        return jsonify({"error": "Not authenticated"}), 401

    # status = Functions.canvasPages.downloadPageToDrive(courseID, canvasPage)
    file = canvas.convertPageToFile(courseID, canvasPage)
    googleFunctions.uploadToDrive(file)
    status = "Successfully exported canvas page and imported it to google drive"
    return {"Response": status}


# Exports a specified Google Drive File and imports it as a Canvas Page
@app.route("/getDriveFileToCanvas", methods=["GET", "POST"])
def downloadFileToCanvas():
    """Exports a specified Google Drive File and imports it as a Canvas Page"""
    response = request.get_json(force=True)
    courseID = response["courseID"]
    googleFileID = response["Google_FileID"]
    googleFile = response["Google_File"]

    # status = Functions.canvasPages.downloadFromDriveToCanvasPage(
    # courseID, googleFileID, googleFile)
    fileContent, fileName = googleFunctions.getFileContent(googleFileID, googleFile)
    if fileContent == "Error":
        return {"Response": "There was an error finding the google file."}
    canvas = get_canvas_instance()
    if canvas is None:
        return jsonify({"error": "Not authenticated"}), 401
    canvas.createPage(courseID, fileName, fileContent)
    status = "Successfully created canvas page from google drive file"
    return {"Response": status}


# Creates a Google Drive Folder
@app.route("/createGoogleFolder", methods=["GET", "POST"])
def createGoogleFolder():
    """Creates a Google Drive Folder"""
    response = request.get_json(force=True)
    courseID = response["courseID"]
    folderName = response["folderName"]
    try:
        parentFolder = response["parentFolder"]
    except:
        return {"Response": "Parent Folder was not chosen"}
    # status = Functions.googleFile.createDriveFolder(
    #     courseID, folderName, parentFolder)
    status = googleFile.createDriveFolder(courseID, folderName, parentFolder)
    try:
        return {
            "Folder": status,
            "Response": ("Folder '" + status["name"] + "' created"),
        }
    except:
        return {"Response": status}


# Creates a Google Drive Folder
@app.route("/createSharedGoogleFolder", methods=["GET", "POST"])
def createSharedGoogleFolder():
    """Creates a shared Google Drive Folder"""
    response = request.get_json(force=True)
    courseID = response["courseID"]
    access = response["access"]

    try:
        parentFolder = response["parentFolder"]
        _ = parentFolder[0]["id"]
    except KeyError as e:
        return {"Response": "Parent Folder was not chosen"}

    if access == "":
        return {"Response": "Access option was not chosen"}
    canvas = get_canvas_instance()
    if canvas is None:
        return jsonify({"error": "Not authenticated"}), 401
    courseName = canvas.getCourse(courseID).name
    # folderName = courseID + " " + canvasFunctions.courseName(courseID)
    folderName = courseID + " " + courseName

    if parentFolder[0]["mimeType"] != "application/vnd.google-apps.folder":
        return {"Response": "Error: Parent Folder can not be a file"}

    roster = response["roster"]
    if not (roster):
        return {"Response": "Roster was not provided"}
    """This is so that I am not spamming Sean and Brian with emails"""
    # roster = [{'id': 4221108, 'email': 'ajdeehring@gmail.com'},
    #         {'id': 4221713, 'email': 'adam.deehring@gmail.com'}]

    # folder = Functions.googleFile.createDriveFolder(
    #     courseID, folderName, parentFolder)
    # status = Functions.googleFunctions.updateSharesOnFolder(
    #     roster, folder, access)
    folder = googleFile.createDriveFolder(courseID, folderName, parentFolder)
    status = googleFunctions.updateSharesOnFolder(roster, folder, access)
    return {"Response": status, "Folder": folder}


# Deletes a Google Drive file
@app.route("/deleteGoogleFolder", methods=["GET", "POST"])
def deleteGoogleFolder():
    """Deletes a Google Drive File"""
    response = request.get_json(force=True)
    folderID = response["folderID"]
    # status = Functions.googleFile.deleteDriveFolder(folderID)
    status = googleFile.deleteDriveFolder(folderID)
    return {"Response": status}


# Updates shares on a folder from Google Drive
@app.route("/updateSharesOnFolder", methods=["GET", "POST"])
def updateSharesOnFolder():
    """Updates shares on a folder from Google Drive"""
    response = request.get_json(force=True)
    access = response["access"]
    if access == "":
        return {"Response": "Access option was not chosen"}
    roster = response["roster"]
    if not (roster):
        return {"Response": "Roster was not provided"}

    try:
        file = response["file"][0]
    except KeyError:
        return {"Response": "Please Select A File to Upload"}
    if roster == "Course was Not Found":
        return {"Response": "Course was Not Found"}
    if roster == "No Emails Found":
        return {"Response": "No Email Found"}
    # status = Functions.googleFunctions.updateSharesOnFolder(
    #     roster, file, access)
    status = googleFunctions.updateSharesOnFolder(roster, file, access)
    return {"Response": status}


# Updates shares on a folder from Google Drive
@app.route("/createGroupGoogleFolders", methods=["GET", "POST"])
def createGroupGoogleFolders():
    """Updates shares on a folder from Google Drive"""
    response = request.get_json(force=True)
    groups = response["groups"]
    courseID = response["courseID"]
    access = response["access"]

    try:
        parentFolder = response["parentFolder"]
        _ = parentFolder[0]["id"]
    except KeyError as e:
        return {"Response": "Parent Folder was not chosen"}

    if access == "":
        return {"Response": "Access option was not chosen"}

    if parentFolder[0]["mimeType"] != "application/vnd.google-apps.folder":
        return {"Response": "Error: Parent Folder can not be a file"}
    canvas = get_canvas_instance()
    if canvas is None:
        return jsonify({"error": "Not authenticated"}), 401

    courseName = canvas.getCourse(courseID).name
    # statuses = []
    # for group in groups:
    #     # folderName = canvasFunctions.courseName(courseID) + " " + group
    #     folderName = courseName + " " + group
    #     folder = googleFile.createDriveFolder(
    #         courseID, folderName, parentFolder)
    #     status = googleFunctions.updateSharesOnFolder(
    #         groups[group], folder, access)
    #     statuses.append(status)

    # status = "All Folders Created. " + str(statuses.count("Success")) + "/" + str(
    #     len(statuses)) + " Group Folders Successfully Shared"
    status = googleFunctions.createGroupFolders(
        courseID, courseName, groups, parentFolder, access
    )
    return {"Response": status}


# Import file from Google Drive to Canvas, File has already been selected
@app.route("/downloadGoogleFile", methods=["GET", "POST"])
def downloadGoogleFile():
    """
    Import file from Google Drive to Canvas,
    File has already been selected
    """
    response = request.get_json(force=True)
    courseID = response["courseID"]
    try:
        allFiles = response["file"]
    except KeyError:
        return {"Response": "Please Select A File to Upload"}
    destFolder = response["destFolder"]
    canvas = get_canvas_instance()
    if canvas is None:
        return jsonify({"error": "Not authenticated"}), 401
    # status = Functions.googleFile.uploadToCanvas(
    #     courseID, allFiles, destFolder)
    status = googleFile.uploadToCanvas(courseID, allFiles, destFolder, canvas)
    try:
        for file in allFiles:
            os.remove(file["name"])
    except FileNotFoundError as error:
        pass
    return {"Response": status}


# Import Workspace file from Google Drive to Canvas, File has already been selected
@app.route("/downloadWorkspaceFile", methods=["GET", "POST"])
def downloadWorkspaceFile():
    """
    Import Workspace file from Google Drive to Canvas,
    File has already been selected
    """
    response = request.get_json(force=True)
    courseID = response["courseID"]
    try:
        allFiles = response["file"]
    except KeyError:
        return {"Response": "Please Select A File to Upload"}
    destFolder = response["destFolder"]
    canvas = get_canvas_instance()
    if canvas is None:
        return jsonify({"error": "Not authenticated"}), 401
    # status = Functions.googleWorkspaceFile.uploadToCanvas(
    #     courseID, allFiles, destFolder)
    status = googleWorkspaceFile.uploadToCanvas(courseID, allFiles, destFolder, canvas)
    try:
        for file in allFiles:
            _, fileType = googleCore.determineFileType(file["mimeType"])
            os.remove(file["name"] + fileType)
    except FileNotFoundError as error:
        pass
    return {"Response": status}


# Exports Syllabus file of a course and imports it to local directory or as a Google Drive File
@app.route("/getSyllabus", methods=["GET", "POST"])
def downloadCourseSyllabus():
    """
    Exports Syllabus file of a course and imports it to local directory
    and as a Google Drive File
    """
    response = request.get_json(force=True)
    courseID = response["courseID"]
    downloadToLocal = response["toLocal"]
    canvas = get_canvas_instance()
    if canvas is None:
        return jsonify({"error": "Not authenticated"}), 401
    file = canvas.getSyllabus(courseID)
    if file is None:
        return {"Response": "File not found."}
    # status = Functions.canvasSyllabus.downloadSyllabus(
    #     courseID, files, downloadToLocal)
    googleFunctions.uploadToDrive(file, downloadToLocal)
    if downloadToLocal == True:
        status = (
            "Uploaded Syllabus file to Google Drive and saved to your Local machine."
        )
    else:
        status = "Uploaded Syllabus file to Google Drive."
    return {"Response": status}


# Creates a Course Folder
@app.route("/createCanvasFolder", methods=["GET", "POST"])
def createCanvasFolder():
    """creates a Canvas folder"""
    response = request.get_json(force=True)
    courseID = response["courseID"]
    folderName = response["folderName"]
    parentFolder = response["parentFolder"]
    canvas = get_canvas_instance()
    if canvas is None:
        return jsonify({"error": "Not authenticated"}), 401
    # status = canvasFunctions.createCanvasFolder(
    #     courseID, folderName, parentFolder)
    status = canvas.createCourseFolder(courseID, folderName, parentFolder)
    try:
        return {
            "Folder": status,
            "Response": ("Folder '" + status["name"] + "' created"),
        }
    except:
        return {"Response": status}


# Deletes a Folder
@app.route("/deleteCanvasFolder", methods=["GET", "POST"])
def deleteCanvasFolder():
    """deletes a Canvas folder"""
    response = request.get_json(force=True)
    folderID = response["folderID"]
    canvas = get_canvas_instance()
    if canvas is None:
        return jsonify({"error": "Not authenticated"}), 401
    # status = canvasFunctions.deleteCanvasFolder(folderID)
    status = canvas.deleteFolder(folderID)
    return {"Response": status}


# ----------------------------------Quiz App Routes-------------------------------------------------------------
# Export a list of the course's quizzes as a .csv file
@app.route("/exportQuizzes", methods=["GET", "POST"])
def getQuizzes():
    """exports a list of the course's quizzes as a csv file"""
    response = request.get_json(force=True)
    courseID = response["courseID"]
    canvas = get_canvas_instance()
    if canvas is None:
        return jsonify({"error": "Not authenticated"}), 401
    status = canvas.exportQuizListCSV(courseID)
    return {"Response": status}


# Returns a list of all the courses quizzes
@app.route("/listQuizzes", methods=["POST", "GET"])
def getAllQuizzes():
    """returns a list of all the course quizzes"""
    response = request.get_json(force=True)
    courseID = response["courseID"]
    Quizzes = []
    canvas = get_canvas_instance()
    if canvas is None:
        return jsonify({"error": "Not authenticated"}), 401
    quizList = canvas.getQuizzes(courseID)
    for quiz in quizList:
        entry = {"name": quiz.get("title"), "id": quiz.get("id")}
        Quizzes.append(entry)
    return jsonify(response=Quizzes)


# Exports all student submissions for a specified quiz as a .csv file
@app.route("/downloadQuizSubmissions", methods=["POST", "GET"])
def downloadQuizSubmissions():
    """exports all student submissions for a specified quiz as a csv file"""
    response = request.get_json(force=True)
    courseID = response["courseID"]
    quizID = response["Quiz_ID"]
    canvas = get_canvas_instance()
    if canvas is None:
        return jsonify({"error": "Not authenticated"}), 401
    # status = Functions.canvasQuizzes.QuizManager(courseID, quizID)
    status = canvas.downloadQuizSubmissionsCSV(courseID, quizID)
    return {"Response": status}


# ----------------------------------Assignment App Routes-------------------------------------------------------------
# Export a list of the course's assignments as a .csv file
@app.route("/exportAssignments", methods=["GET", "POST"])
def getAssignments():
    """exports a list of the course's assignments as a csv file"""
    response = request.get_json(force=True)
    courseID = response["courseID"]
    canvas = get_canvas_instance()
    if canvas is None:
        return jsonify({"error": "Not authenticated"}), 401
    status = canvas.exportAssignmentListCSV(courseID)
    return {"Response": status}


# Returns a list of all the assignments in a course
@app.route("/listAssignments", methods=["POST", "GET"])
def getAllAssignments():
    """returns a list of all the assignments in a course"""
    response = request.get_json(force=True)
    courseID = response["courseID"]
    Assignments = []
    canvas = get_canvas_instance()
    if canvas is None:
        return jsonify({"error": "Not authenticated"}), 401
    assignmentList = canvas.getAssignmentsData(courseID)
    for assignment in assignmentList:
        entry = {"name": assignment.get("name"), "id": assignment.get("id")}
        Assignments.append(entry)
    return jsonify(response=Assignments)


# Exports all student submissions of a specified assignment as a .csv file
@app.route("/downloadAssignmentSubmissions", methods=["POST", "GET"])
def downloadAssingmentSubmissions():
    """creates a csv file of student submissions for a specified assignment"""
    response = request.get_json(force=True)
    courseID = response["courseID"]
    assignmentID = response["Assignment_ID"]
    canvas = get_canvas_instance()
    if canvas is None:
        return jsonify({"error": "Not authenticated"}), 401
    # status = Functions.canvasAssignments.assignmentManager(
    #     courseID, assignmentID)
    status = canvas.downloadAssignmentSubmissionsCSV(courseID, assignmentID)
    return {"Response": status}


# -------------------------------------Canvas App Routes----------------------------------------------------------
# Returns a list of all the folders in a course
@app.route("/courseFolders", methods=["GET", "POST"])
def courseFolders():
    """returns a list of all the folders in a course"""
    response = request.get_json(force=True)
    courseID = response["courseID"]
    canvas = get_canvas_instance()
    if canvas is None:
        return jsonify({"error": "Not authenticated"}), 401
    folders = canvas.getFoldersList(courseID)
    return jsonify(response=folders)


# Returns a list of all the course's Pages in the 'Page' tab
@app.route("/canvasCoursePages", methods=["GET", "POST"])
def canvasPages():
    """returns a list of a course's Pages in the 'Page' tab"""
    response = request.get_json(force=True)
    courseID = response["courseID"]
    canvasPages = []
    canvas = get_canvas_instance()
    if canvas is None:
        return jsonify({"error": "Not authenticated"}), 401
    pagesList = canvas.getPagesData(courseID)
    for page in pagesList:
        entry = {"name": page.get("title"), "id": page.get("page_id")}
        canvasPages.append(entry)
    return jsonify(response=canvasPages)


# -----------------------------------------------------------------------------------------------
# Returns to the front end with courses listed as favorites for the user to choose from
@app.route("/courseFavorites")
def coursesFavorites():
    """returns a list of favorited courses"""
    app.logger.info("A user requested favorite courses")
    canvas = get_canvas_instance()
    if canvas is None:
        return jsonify({"error": "Not authenticated"}), 401
    favorites = canvas.getFavorites()
    return jsonify(courses=favorites)


# -----------------------------------------------------------------------------------------------
# Imports groups into Canvas via a csv file
@app.route("/importStudentGroups", methods=["GET", "POST"])
def importStudents():
    """imports groups into Canvas via a csv file"""
    courseID = request.form.get("courseId")
    # response = request.files.get('file')
    try:
        file = request.files["file"]
    except KeyError:
        return {"Response": "Please Select A File to Upload"}
    canvas = get_canvas_instance()
    if canvas is None:
        return jsonify({"error": "Not authenticated"}), 401

    result = canvas.importStudentGroups(courseID, file)
    # return Functions.importStudents.importManager()
    if result == "success":
        return jsonify(message="Groups created", status_code=200)
    return jsonify(message="Failed", status_code=500)


# -----------------------------------------------------------------------------------------------
# Creates a csv file full of students and their groups from a specified course
@app.route("/exportStudentGroups", methods=["GET", "POST"])
def exportStudentGroups():
    """creates a csv file of students and their groups from a specified course"""
    response = request.get_json(force=True)
    courseID = response.get("course")
    if request.method == "POST":
        canvas = get_canvas_instance()
        if canvas is None:
            return jsonify({"error": "Not authenticated"}), 401
        result = canvas.exportGroupsCSV(courseID)
        # return Functions.exportStudents.exportManager()
        if result == "success":
            return jsonify(message="Created CSV", status_code=200)
        return jsonify(message="CSV creation failed", status_code=500)


# -----------------------------------------------------------------------------------------------
# Exports a json of the students with a given key
@app.route("/exportStudents", methods=["GET", "POST"])
def exportStudentsJson():
    """exports a JSON of the students in a course with a given key"""
    response = request.get_json(force=True)
    courseId = response["courseId"]
    targetKey = response["key"]
    canvas = get_canvas_instance()
    if canvas is None:
        return jsonify({"error": "Not authenticated"}), 401
    # roster = Functions.exportStudents.getCourseRoster(courseId, key=targetKey)
    roster = canvas.exportStudents(courseId, key=targetKey)
    return {"Response": roster}


# -----------------------------------------------------------------------------------------------
# Exports a json of the students with a given key
@app.route("/exportGroups", methods=["GET", "POST"])
def exportGroupsJson():
    """exports a JSON of all groups and their members with a given key"""
    response = request.get_json(force=True)
    courseId = response["courseId"]
    targetKey = response["key"]
    canvas = get_canvas_instance()
    if canvas is None:
        return jsonify({"error": "Not authenticated"}), 401
    # roster = Functions.exportStudents.getGroups(courseId, key=targetKey)
    roster = canvas.exportGroupsJSON(courseId, key=targetKey)
    return {"Response": roster}


# -----------------------------------------------------------------------------------------------
# Exports a json of the students with a given key
@app.route("/exportGroup", methods=["GET", "POST"])
def exportGroupJson():
    """exports a JSON of a group and its members with a given key"""
    response = request.get_json(force=True)
    print(response)
    courseId = response["courseId"]
    targetKey = response["key"]
    teamName = response["teamName"]
    canvas = get_canvas_instance()
    if canvas is None:
        return jsonify({"error": "Not authenticated"}), 401
    # roster = Functions.exportStudents.getGroups(courseId, key=targetKey)
    roster = canvas.exportGroupsJSON(courseId, key=targetKey)
    try:
        group = roster[teamName]
    except KeyError:
        return {"Response": "No Group Found"}

    return {"Response": group}


# Returns a list of all the groups in a course
@app.route("/listGroups", methods=["POST", "GET"])
def getAllGroups():
    """returns a list of all the groups in a course"""
    response = request.get_json(force=True)
    courseID = response["courseID"]
    canvas = get_canvas_instance()
    if canvas is None:
        return jsonify({"error": "Not authenticated"}), 401
    groups = canvas.getGroupsList(courseID)
    return jsonify(response=groups)


# -----------------------------------------------------------------------------------------------
# Creates a csv file full of a courses students and their id for use in importing student groups
@app.route("/exportCourseRoster", methods=["GET", "POST"])
def exportCourseRoster():
    """Creates a csv file of a course's student names and their ids for use in
    importing student groups
    """
    if request.method == "POST":
        response = request.get_json(force=True)
        courseID = response.get("courseId")
        canvas = get_canvas_instance()
        if canvas is None:
            return jsonify({"error": "Not authenticated"}), 401

        result = canvas.exportCourseRoster(courseID)
        # return Functions.exportStudents.courseRoster()
        if result == "success":
            return jsonify(message="Created CSV", status_code=200)
        return jsonify(message="CSV creation failed", status_code=500)


# -----------------------------------------------------------------------------------------------
# Called if importing settings diectly from a favorited course
@app.route("/settings", methods=["GET", "POST"])
def settings():
    """called if importing settings directly from a favorited course"""
    if request.method == "POST":
        response = request.get_json(force=True)
        exportCourse = response.get("courseId")
        importCourse = response.get("importCourse")
        canvas = get_canvas_instance()
        if canvas is None:
            return jsonify({"error": "Not authenticated"}), 401
        result = canvas.importSettingsFromCourse(exportCourse, importCourse)
        # return Functions.canvasSettings.settingsManager()
        if result == "success":
            return jsonify(
                message="Course Settings and Navigation imported", status_code=200
            )
        return jsonify(message="Failed", status_code=500)


# -----------------------------------------------------------------------------------------------
# Called if exporting settings and navigation to .json files
@app.route("/exportSettings", methods=["GET", "POST"])
def exportSettings():
    """called if exporting settings and navigation to .json files"""
    if request.method == "POST":
        response = request.get_json(force=True)
        exportCourse = response.get("courseId")
        canvas = get_canvas_instance()
        if canvas is None:
            return jsonify({"error": "Not authenticated"}), 401
        result = canvas.exportSettingsToFile(exportCourse)
        # return Functions.canvasSettings.toFile()
        if result == "success":
            return jsonify(
                message="Course Settings and Navigation exported to files",
                status_code=200,
            )
        return jsonify(message="Failed", status_code=500)


# -----------------------------------------------------------------------------------------------
# Called if importing settings and navigation from files
@app.route("/settingsFromFiles", methods=["GET", "POST"])
def settingsFromFiles():
    """Called if importing settings and navigation from files"""
    if request.method == "POST":
        courseID = request.form.get("courseId")
        settingsFile = request.files.get("settingsFile")
        navFile = request.files.get("navFile")
        canvas = get_canvas_instance()
        if canvas is None:
            return jsonify({"error": "Not authenticated"}), 401
        result = canvas.importSettingsFromFiles(courseID, settingsFile, navFile)
        # return Functions.canvasSettings.fromFiles()
        if result == "success":
            return jsonify(
                message="Imported settings and navigation to course.", status_code=200
            )
        return jsonify(message=result, status_code=500)


# -----------------------------------------------------------------------------------------------
# Retrieve a list of active courses for the current user
@app.route("/getCourses")
def getCourses():
    """retrieve a list of active courses for the current user"""
    subset = ("name", "id")
    canvas = get_canvas_instance()
    if canvas is None:
        return jsonify({"error": "Not authenticated"}), 401
    courses = canvas.getCoursesData(subset)
    return jsonify(courses=courses)


# ------------------------------------------------------------------------------
### Author: Pooja Pal
# -----------------------------------------------------------------------------


# -------------------------------------Canvas Roles App Routes------------------
# retrieve the list of distinct roles that the current user has on diferent courses
@app.route("/getDistinctRoles", methods=["GET", "POST"])
def getDistinctRoles():
    """retrieve the list of distinct roles that the current user has on diferent courses"""
    if request.method == "GET":
        canvas = get_canvas_instance()
        if canvas is None:
            return jsonify({"error": "Not authenticated"}), 401
        roles = canvas.listDistinctRoles()
        return jsonify(roles=roles)


# -------------------------------------Canvas Courses----------------------
# fetches the distinct terms  that has one or more enrollments
@app.route("/getTerms", methods=["GET", "POST"])
def getTerms():
    """retrieve the list of the the distinct terms  that has one or more enrollments"""
    if request.method == "GET":
        canvas = get_canvas_instance()
        if canvas is None:
            return jsonify({"error": "Not authenticated"}), 401
        courseTerms = canvas.getTerms()
    return jsonify(courseTerms)


# lists all the students for a particular course
@app.route("/getCourseStudents", methods=["GET", "POST"])
def getCourseStudents():
    """lists all the students in the courses"""
    if request.method == "POST":
        request_json = request.get_json(force=True)
        canvas = get_canvas_instance()
        if canvas is None:
            return jsonify({"error": "Not authenticated"}), 401
        studentList = canvas.getCourseStudents(request_json)
    return jsonify(response=studentList)


# fetches list of assignments in the course
@app.route("/getAssignments", methods=["GET", "POST"])
def listAssignments():
    """fetches the available assignment data in the courses"""
    if request.method == "POST":
        request_json = request.get_json(force=True)
        canvas = get_canvas_instance()
        if canvas is None:
            return jsonify({"error": "Not authenticated"}), 401
        assignments = canvas.listAssignments(request_json)
    return jsonify(response=assignments)


# -------------------------------------Assignments----------------------
# fetches the metadata such as numbe of attempts, acceptable files and other data about the assignments
@app.route("/getAssignmentMetadata", methods=["GET", "POST"])
def getAssignmentMetadata():
    """fetches the metadata such as numbe of attempts, acceptable files and other data about the assignments"""
    if request.method == "POST":
        request_json = request.get_json(force=True)
        canvas = get_canvas_instance()
        if canvas is None:
            return jsonify({"error": "Not authenticated"}), 401
        assignmentMetadata = canvas.getAssignmentMetadata(request_json)
        return assignmentMetadata


# fetches the logged in users name and id as that it as be shown as a default submitter name
@app.route("/getSubmitterData", methods=["GET", "POST"])
def getSubmitterData():
    """fetches the logged in users name and id as that it as be shown as a default submitter name"""
    if request.method == "GET":
        canvas = get_canvas_instance()
        if canvas is None:
            return jsonify({"error": "Not authenticated"}), 401

        submitterData = canvas.getSubmitterData()
    return submitterData


# --------------------Assignment submission -------------------------------------------------------
# In UI when the user selects the file or files they get uploaded in canvas user's temporary storage
@app.route("/uploadSubmissionFiles", methods=["GET", "POST"])
def uploadSubmissionFiles():
    if request.method == "POST":
        """uploads files to the canvas local storage that is then used for submission"""
        file = request.files["file"]
        canvas = get_canvas_instance()
        if canvas is None:
            return jsonify({"error": "Not authenticated"}), 401

        result = canvas.uploadSubmissionFiles(request, file)
    return jsonify(response=result)


# Submits an Assignment in the canvas
@app.route("/submitAssignment", methods=["GET", "POST"])
def submitAssignment():
    if request.method == "POST":
        """Submission an assignmnet to the canvas"""
        request_json = request.get_json(force=True)

        canvas = get_canvas_instance()
        if canvas is None:
            return jsonify({"error": "Not authenticated"}), 401

        workflow_state = canvas.submitAnAssignment(request_json)
    return jsonify(response=workflow_state)


# --------------------Export Contributors -------------------------------------------------------
#  Assignments comments will have the contributors data. This API will export them to a csv file
@app.route("/getGrpfromComments", methods=["GET", "POST", "PUT"])
def exportTeamfrmCmts():
    """Exports the contributors details in a csv file"""
    if request.method == "POST":
        request_json = request.get_json(force=True)

        canvas = get_canvas_instance()
        if canvas is None:
            return jsonify({"error": "Not authenticated"}), 401

        team_info = canvas.exportTeamfrmCmts(request_json)
    return jsonify(response=team_info)


# --------------------Export Syllabus -------------------------------------------------------
#  Canvas course has the syllabus Page. It exports the Syllabus into a pdf and zips them up
@app.route("/exportSyllabus", methods=["GET", "POST"])
def exportSyllabus():
    """Exports the canvas syllabus Page for a perticular course"""
    if request.method == "POST":
        request_json = request.get_json(force=True)
        exportType = request_json["exportType"]
        if "toPDF" == exportType:
            canvas = get_canvas_instance()
            if canvas is None:
                return jsonify({"error": "Not authenticated"}), 401

            response = canvas.exportSyllabusToPdf(request_json)
            if response == None:
                return {"response": "Syllabus has been exported successfully!!"}
            return {"response": response}
        elif "toDB" == exportType:
            print("DB export to be developed")
    return []


# Lists the course names that the current logged in user is enrolled in
@app.route("/courses")
def getCourseNames():
    """Lists the courses with itscourse name and id"""

    canvas = get_canvas_instance()
    if canvas is None:
        return jsonify({"error": "Not authenticated"}), 401

    courseNames = canvas.getCourseNames()
    return jsonify(response=courseNames)


# Lists the course names and IDs that the current logged in user is enrolled in
@app.route("/coursesAndID")
def getCourseNamesAndID():
    """Lists the courses with itscourse name and id"""

    canvas = get_canvas_instance()
    if canvas is None:
        return jsonify({"error": "Not authenticated"}), 401

    courseNames = canvas.getCourseNamesID()
    return jsonify(response=courseNames)


# ------------------------------------------------------------------------------


# -------------AUTHOR: Karan Chopra--------QTI import/export quiz Management-----------------------------------------------------
# Used for import the quiz in the QTI format.
@app.route("/importQTIQuiz", methods=["POST"])
def importQTIQuiz():
    # getting the file and the quiz name from the request along with the courseId
    courseId = request.form.get("courseId")
    quizName = request.form.get("quizName")
    # if "file" not in request.files:
    #   return "No file selected!"
    # file = request.files["file"]
    # if file.filename == "":
    # return "No file selected!"
    canvas = get_canvas_instance()
    # this function below will convert our file into Qti format and then call the canvas API
    result = canvas.importQuizFromQTI(courseId, quizName)
    # result the status of the quiz import SUCCESS or FAILURE
    return result


@app.route("/exportQTIQuiz", methods=["POST"])
def exportQTIQuiz():
    # get quizID from user through form
    quizId = request.form.get("quizId")
    courseId = request.form.get("courseId")
    if quizId == "":
        return {"error": "no quiz selected"}
    canvas = get_canvas_instance()
    result = canvas.export_QTIQuiz(quizId, courseId)
    return result


@app.route("/exportAllQTI", methods=["POST"])
def exportAllQTI():
    # get the course id
    courseId = request.form.get("courseId")
    canvas = get_canvas_instance()
    result = canvas.exportEveryQti(courseId)
    return result

def parse_text_content(text_content , isXml = False):
    questions = []
    current_question = None
    current_options = {}
    gap=1
    if(isXml):
        gap=0
    lines = text_content.split('\n')
    for i, line in enumerate(lines):
        line = line.strip()
        if line.startswith("Question"):
            if current_question is not None:
                questions.append({"question": current_question, "options": current_options})
                current_options = {}
            # Look for the next line if the current line starts with "Question"
            current_question = lines[i + gap].strip()
        elif line.startswith(("A)", "B)", "C)", "D)")):
            option_letter = line[0]
            option_text = line[3:].strip()
            current_options[option_letter] = option_text

    # Append the last question after the loop
    if current_question is not None:
        questions.append({"question": current_question, "options": current_options})

    return questions


def createQuestions(questionsObj,quizId):
    print('hello world')
    headers = {
        "Authorization": "Bearer 10~dVERK37nMXapiXX17crpLcI5jJhufVIAnEw2MacMgxR8nnuGwo8xaGVz3Lm8VSRW"
    }
    for question in questionsObj:
        quesPayload = {
            "question":{
                "question_text":question['question'],
                "question_type":'multiple_choice_question',
                "answers":[{
                    "text": question['options']['A'],
                },
                {
                "text":question['options']['B'],
                },
                {
                 "text":question['options']['C'],
                },
                {
                 "text":question['options']['D'],
                }]
            }
        }
        quesRes = requests.post(
        "https://canvas.uw.edu/api/v1/courses/1521081/quizzes/{}/questions".format(quizId),
        json=quesPayload,
        headers=headers
        )

@app.route('/testing' , methods=["POST"])
def testing():
    quizName = request.form.get('quizName')
    if "file" not in request.files:
        return "No file selected!"
    file = request.files["file"]
    if file.filename == "":
        return "No file selected!"
    headers = {
        "Authorization": "Bearer 10~dVERK37nMXapiXX17crpLcI5jJhufVIAnEw2MacMgxR8nnuGwo8xaGVz3Lm8VSRW"
    }
    payload = {
        "quiz": {
            "title": "{}".format(quizName),  # Replace with your quiz title
        }
    }
    result = requests.post(
        "https://canvas.uw.edu/api/v1/courses/1521081/quizzes",
        json=payload,
        headers=headers,
    )
    res = result.json()
    file_content = file.read().decode('utf-8')
    quiz_data = parse_text_content(file_content)
    quizId = res['id']
    createQuestions(quiz_data , quizId)
    return {"res": res["id"]}

###################################
################################
import lxml.etree as etree
from werkzeug.datastructures import FileStorage

def process_xml_file(xml_file):
    output_filename = 'processed_qti_data.txt'
    
    # Parse the XML file
    tree = etree.parse(xml_file)
    root = tree.getroot()

    # Namespace map extraction: 'None' key is used for default namespace if present
    namespaces = {'ns': root.nsmap[None]} if None in root.nsmap else {}

    # Open a file to write the processed data
    with open(output_filename, 'w') as file:
        items = root.xpath('//ns:item', namespaces=namespaces)
        for item in items:
            title = item.get('title')
            file.write(f'Question {title}:\n')

            # Extracting response options within the item
            responses = item.xpath('.//ns:response_label', namespaces=namespaces)
            correct_answer_text = None
            if responses:
                for response in responses:
                    response_ident = response.get('ident')
                    is_correct = response.get('correct') == 'true'
                    mattext = response.xpath('.//ns:mattext', namespaces=namespaces)
                    text_content = mattext[0].text if mattext else "No text available"
                    file.write(f'  {response_ident}. {text_content}\n')
                    if is_correct:
                        correct_answer_text = text_content
            else:
                file.write('  No responses available.\n')
            
            # Writing the correct answer
            if correct_answer_text:
                file.write(f'Correct Answer: {correct_answer_text}\n')
            file.write('----------------\n')

    print(f'Data processed and saved to {output_filename}.')

import xml.etree.ElementTree as ET
@app.route("/parsing", methods=["POST"])
def testingg():
    #get details from frontEnd
    quizName = request.form.get('quizName')
    if "file" not in request.files:
        return "No file selected!"
    file = request.files["file"]
    if file.filename == "":
        return "No file selected!"

    headers = {
        "Authorization": "Bearer 10~dVERK37nMXapiXX17crpLcI5jJhufVIAnEw2MacMgxR8nnuGwo8xaGVz3Lm8VSRW"
    }
    payload = {
        "quiz": {
            "title": "{}".format(quizName),  # Replace with your quiz title
        }
    }
    result = requests.post(
       "https://canvas.uw.edu/api/v1/courses/1521081/quizzes",
       json=payload,
       headers=headers,
    )
    res = result.json()
    quizId = res['id']
    # Extract content from the XML
    process_xml_file(file)
    with open('processed_qti_data.txt', 'r') as file:
        content = file.read()
    app.logger.info(content)
    quizData = parse_text_content(content , True)
    app.logger.info(quizData)
    createQuestions(quizData , quizId) 
    return {"try":"to make a quiz from a qti file"} 

if __name__ == "__main__":
    app.run(debug=True)
    # ------------------------------------------------------------------------------------------------------------------------------------

