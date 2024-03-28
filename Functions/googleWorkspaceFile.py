import Functions.canvasFunctions as canvasFunctions
from core.canvas_services import canvas_services as canvasCore
from core.google_core import google_services as googleCore


def uploadToCanvas(courseId, file, destFolder):

    folderID = canvasFunctions.getFolderID(courseId, destFolder)
    if (folderID == "Error"):
        return ("Course was Not Found")
    elif (folderID == -1):
        return ("Folder was Not Found")
    URL = canvasFunctions.generateFolderURL(folderID)

    countOfSuccesses = 0
    for fileToUpload in file:
        targetFileType, targetFileExt = googleCore.determineFileType(
            fileToUpload['mimeType'])
        newFileName = fileToUpload['name'] + targetFileExt
        try:
            f = open(newFileName, 'xb')
        except FileExistsError:
            return ("File Already Exist")
        except FileNotFoundError:
            return ("File Not Found")

        f.write(googleCore.exportWorkspaceFile(
            fileToUpload['id'], targetFileType))
        if (f == None):
            return ("File Download Error")
        status = canvasCore.uploadToCanvasFile(
            URL, newFileName, targetFileType)
        if status == "Success":
            countOfSuccesses += 1

    if (countOfSuccesses == len(file)):
        return ("Successfully Uploaded All Files to Target Destination: " + str(countOfSuccesses) + " file(s) successfully uploaded ")
    if (countOfSuccesses < len(file)):
        return ("Error Occured when Uploaded All Files to Target Destination: " + str(countOfSuccesses) + " file(s) successfully uploaded ")
