from core.canvas_services import canvas_services as canvasCore

# returns the users courses


def courses():
    return canvasCore.getCourses()

# -----------------------------------------------------------------------------------------------
# returns the specified courses id from the users course list


def courseId(name):
    id = "None"
    courses = canvasCore.getCourses()
    for course in courses:
        if course.get('name') == name:
            id = course.get('id')
            break
    return id

# -----------------------------------------------------------------------------------------------
# Returns the name of the course


def courseName(courseID):
    course = canvasCore.getCoursesName(courseID)
    if(course == "Error"):
        return ("There was an error finding the course.")
    return course.get('name')

# -----------------------------------------------------------------------------------------------
# returns an array containing all the files from a specified course, in their json format so you can extract the information you need


def getAllFiles(courseID):
    courseFiles = canvasCore.getCanvasFiles(courseID)
    return courseFiles
# -----------------------------------------------------------------------------------------------
# Generates the URL needed to upload a file in a certain canvas folder


def generateFolderURL(folderID):
    return canvasCore.getFolderFilesURL(folderID)

# -----------------------------------------------------------------------------------------------
# Uploads a specific file to a specific folder in Canvas


def uploadFileToCanvas(URL, fileName):
    return canvasCore.uploadToCanvas(URL, fileName)

# -----------------------------------------------------------------------------------------------
# Returns the ID the specified folder


def getFolderID(courseID, folderChoice):
    folders = canvasCore.getFolders(courseID)
    if(folders == "Error"):
        return "Error"
    folderID = -1
    for folder in folders:
        if folderChoice == folder.get("full_name"):
            folderID = folder.get("id")
    if(folderID == -1):
        return -1
    else:
        return str(folderID)

# -----------------------------------------------------------------------------------------------
# Returns a list of all the quizzes in a course


def getQuiz(courseID):
    quizList = canvasCore.getQuizzes(courseID)
    if(quizList == "Error"):
        return ("Error")
    return quizList

# -----------------------------------------------------------------------------------------------
# Returns a list of all the assigments in a course


def getAssignment(courseID):
    assignmentList = canvasCore.getAssignments(courseID)
    if(assignmentList == "Error"):
        return ("There was an error finding the course.")
    return assignmentList

# -----------------------------------------------------------------------------------------------
# Returns the json that involves the canvas page that the user wants to get


def getCanvasPage(courseID, canvasPage):
    response = canvasCore.getPage(courseID, canvasPage)
    if(response == "None"):
        return ("There was an error finding the course.")
    return response

# -----------------------------------------------------------------------------------------------
# Function to create a canvas page


def createCanvasPage(courseID, googleFileTitle, googleFileContent):
    data = {"wiki_page[title]": googleFileTitle,
            "wiki_page[body]": googleFileContent, "wiki_page[published]": "true"}
    return canvasCore.createPage(courseID, data)

# -----------------------------------------------------------------------------------------------
# Function to return the current courses of the user

def courseFavorites():
    favorites = []

    courses = canvasCore.getFavorites()
    for course in courses:
        if course.get('is_favorite') == True:
            entry = {'name': course.get('name'), 'id': course.get('id')}
            favorites.append(entry)
    return favorites

# ---------------------------------------------------------------------------------------
# Function to create a folder

def createCanvasFolder(courseID, folderName, parentFolder):
    parentFolderID = canvasCore.getFolderID(courseID, parentFolder)
    if (parentFolderID == "Error"):
        return ("Course was Not Found")
    elif (parentFolderID == -1):
        return ("Folder was Not Found")
    URL = canvasCore.getFolderFoldersURL(parentFolderID)
    courseFolders = canvasCore.getFolders(courseID)
    for folder in courseFolders:
        if folder['full_name'] == (parentFolder + "/" + folderName):
            return ("Folder already exist with this context")
    return canvasCore.createCourseFolder(URL, {'name': folderName})

# ---------------------------------------------------------------------------------------
# Function to create a folder

def deleteCanvasFolder(folderID):
    URL = canvasCore.getFolderURL(folderID)
    status = canvasCore.deleteCourseFolder(URL)
    if (status != "Error"):
        return ("Success")
    
