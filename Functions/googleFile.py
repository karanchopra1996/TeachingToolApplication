

import Functions.canvasFunctions as canvasFunctions
from core.canvas_services import canvas_services as canvasCore
from core.google_core import google_services as googleCore

def createDriveFolder(courseId, folderName, parentFolder):
    status = googleCore.createDriveFolder(courseId, folderName, parentFolder[0]['id'])
    if status == None:
        return ("Error: Folder was not Created")
    else:
        return status

def deleteDriveFolder(folderID):
    status = googleCore.deleteFile(folderID)
    return status


def uploadToCanvas(courseId, file, destFolder):
    folderID = canvasFunctions.getFolderID(courseId, destFolder)
    if (folderID == "Error"):
        return ("Course was Not Found")
    elif (folderID == -1):
        return ("Folder was Not Found")
    URL = canvasFunctions.generateFolderURL(folderID)

    countOfSuccesses = 0
    for fileToUpload in file:
        try:
            f = open(fileToUpload['name'], 'xb')
        except FileExistsError:
            return ("File Already Exist")
        except FileNotFoundError:
            return ("File Not Found")
        f.write(googleCore.downloadDriveFile(fileToUpload['id']))
        if (f == None):
            return ("File Download Error")
        status = canvasCore.uploadToCanvasFile(
            URL, fileToUpload['name'], fileToUpload['mimeType'])

        if status == "Success":
            countOfSuccesses += 1

    if (countOfSuccesses == len(file)):
        return ("Successfully Uploaded All Files to Target Destination: " + str(countOfSuccesses) + " file(s) successfully uploaded ")
    if (countOfSuccesses < len(file)):
        return ("Error Occured when Uploaded All Files to Target Destination: " + str(countOfSuccesses) + " file(s) successfully uploaded ")
