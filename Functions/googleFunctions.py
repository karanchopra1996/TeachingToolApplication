from core.google_core import google_services as googleCore

# -------------------------------------------------------------------------------
# returns the object you need google access object to then access files from google drive
def getGoogleAccess():
    return googleCore.createGoogleAccess()

# -----------------------------------------------------------------------------------------------
# Function to upload file to google drive as a .docx
def uploadToDrive(fileName):
    googleCore.uploadFileToGoogleDrive(fileName)

# -----------------------------------------------------------------------------------------------
# returns all the files the user has in their google drive
def getGoogleDriveFiles():
    files = googleCore.getGoogleFiles()
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
        return "Successful"
    except:
        return "Error"

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
