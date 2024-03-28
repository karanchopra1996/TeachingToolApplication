from core.google_services import google_services as googleCore
import os
import threading

import google.googleFileContents as gFileContents
from google import googleFile

# -------------------------------------------------------------------------------
# returns the object you need google access object to then access files from google drive
def getGoogleAccess():
    return googleCore.createGoogleAccess()

# -----------------------------------------------------------------------------------------------
# Function to upload file to google drive
def uploadToDrive(fileName, downloadToLocal=False):
    thread = threading.Thread(
        googleCore.uploadFileToGoogleDrive(fileName))
    thread.start()
    thread.join()
    if downloadToLocal is False:
        os.remove(fileName)

# -----------------------------------------------------------------------------------------------
# returns all the files the user has in their google drive
def getGoogleDriveFiles():
    files = googleCore.getGoogleFiles()
    return files

def getFilesList():
    """ Returns a list of the user's Google Drive files """
    fileList = getGoogleDriveFiles()
    files = []
    x = 0
    for file in fileList:
        if file.get('mimeType') == 'application/vnd.google-apps.document':
            entry = {'id': file.get('id'), 'title': (
                file.get('name') + "_" + str(x)), 'type': file.get('mimeType')}
            files.append(entry)
            x = x + 1
    return files

# -------------------------------------------------------------------------------
# Function to call google core function and return the json data connected to the google file name
def findGoogleFile(fileName):
    return googleCore.searchGoogleFiles(fileName)

# -------------------------------------------------------------------------------
# Function to download google file as a .docx
# Currently only works with google drive native files
# TO DO: Find out how to download different file types(.pdf, .doc, .docx, .csv, and etc) from google drive
def downloadGoogleFile(fileID, fileName, mmType):
    service = googleCore.createGoogleAccess()
    try:
        byteData = service.files().export_media(fileId=fileID,
                                                mimeType='application/vnd.openxmlformats-officedocument.wordprocessingml.document').execute()
        if mmType == 'application/pdf':
            newFileName = fileName + ".pdf"
        elif mmType == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            newFileName = fileName + ".docx"
        elif mmType == 'application/vnd.google-apps.document':
            newFileName = fileName + ".docx"
        else:
            newFileName = fileName + ".doc"
        with open(newFileName, 'wb') as f:
            f.write(byteData)
            f.close()
        return newFileName
    except:
        return None

def downloadFile(fileID, fileName, mmType):
    index = fileName.index('_')
    fileName = fileName[0:index]

    fileName = downloadGoogleFile(fileID, fileName, mmType)
    if fileName == None:
        return 'Error'
    else:
        return fileName

# -------------------------------------------------------------------------------
def getFileContent(fileID, fileName):
    """ Retrieve contents of a Google file for use in creating a Canvas page """
    index = fileName.index('_')
    fileName = fileName[0:index]
    fileContents = gFileContents.getFileContents(fileID)
    return (fileContents, fileName)

# -------------------------------------------------------------------------------
# Function to update permissions on a file
def updateSharesOnFolder(roster, file, access):
    if (access == ''):
        return ("Access Option was not selected")
    # 
    # so that I am not spamming Sean and Brian with emails.
    # roster = [{'id': 4221108, 'email': 'ajdeehring@gmail.com'},
    #          {'id': 4221713, 'email': 'adam.deehring@gmail.com'}]
    try:
        if len(roster) != 0:
            status = googleCore.updateShares(file['id'], roster, access)
        else:
            return "No Group Members"
    except KeyError as e:
        return "File was not selected"

    return status

# -------------------------------------------------------------------------------
def createGroupFolders(courseID, courseName, groups, parentFolder, access):
    statuses = []
    for group in groups:
        folderName = courseName + " " + group
        folder = googleFile.createDriveFolder(
            courseID, folderName, parentFolder)
        status = updateSharesOnFolder(
            groups[group], folder, access)
        statuses.append(status)

    status = "All Folders Created. " + str(statuses.count("Success")) + "/" + str(
        len(statuses)) + " Group Folders Successfully Shared"
    return status