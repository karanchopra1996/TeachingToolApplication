import os
import os.path

import Functions.canvasFunctions as canvasFunctions
import Functions.googleFunctions as googleFunctions
#-------------------------------------------------------------------------------
# Function that completes the whole process of exporting a file from google drive and then importing it to canvas files
def uploadToCanvasManager(courseID, fileID, fileName, mimeType, folder):
    index = fileName.index('_')
    fileName = fileName[0:index]

    status = handleGoogleInteraction(fileName, fileID, mimeType)
    if status == "Error":
        return "There was an error finding the google file."
    status = handleCanvasInteraction(courseID, folder, fileName)
    if status == "Error":
        return "There was an error uploading the file to Canvas."
    return ("Successfully imported file to the course.")
#-------------------------------------------------------------------------------
#Function to handle the Google Drive API interactions
def handleGoogleInteraction(fileName, fileID, mimeType):
    response = googleFunctions.downloadGoogleFile(fileID, fileName, mimeType)
    return response
#-------------------------------------------------------------------------------
#Function to handle the Canvas API interactions
def handleCanvasInteraction(courseID, folder, fileName):
    folderId = canvasFunctions.getFolderID(courseID, folder)
    if (folderId == "Error") or (folderId == -1):
        return "An error occurred finding the folder."
    fileName = fileName + ".docx"
    status = fileToCanvas(folderId, fileName)
    return status

#-------------------------------------------------------------------------------
#Function creates the URL to POST to Canvas API
#Then tries posting to Canvas Files Directory
def fileToCanvas(folderId, fileName):
    URL = canvasFunctions.generateFolderURL(folderId)
    status = canvasFunctions.uploadFileToCanvas(URL, fileName)

    os.remove(fileName)

    return status
        