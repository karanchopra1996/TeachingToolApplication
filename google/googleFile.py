from core.google_services import google_services as googleCore

def createDriveFolder(courseId, folderName, parentFolder):
    status = googleCore.createDriveFolder(courseId, folderName, parentFolder[0]['id'])
    if status == None:
        return ("Error: Folder was not Created")
    else:
        return status

def deleteDriveFolder(folderID):
    status = googleCore.deleteFile(folderID)
    return status


def uploadToCanvas(courseID, file, destFolder, canvas):
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

        success, response = canvas.uploadFile(courseID, fileToUpload['name'], 
                content_type=fileToUpload['mimeType'], 
                parent_folder_path=destFolder)
        if success:
            countOfSuccesses += 1

    if (countOfSuccesses == len(file)):
        return ("Successfully Uploaded All Files to Target Destination: " + str(countOfSuccesses) + " file(s) successfully uploaded ")
    if (countOfSuccesses < len(file)):
        return ("Error Occured when Uploaded All Files to Target Destination: " + str(countOfSuccesses) + " file(s) successfully uploaded ")
