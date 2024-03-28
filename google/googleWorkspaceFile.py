from core.google_services import google_services as googleCore


def uploadToCanvas(courseID, file, destFolder, canvas):
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

        success, response = canvas.uploadFile(courseID, newFileName, 
                content_type=targetFileType, 
                parent_folder_path=destFolder)
        if success:
            countOfSuccesses += 1

    if (countOfSuccesses == len(file)):
        return ("Successfully Uploaded All Files to Target Destination: " + str(countOfSuccesses) + " file(s) successfully uploaded ")
    if (countOfSuccesses < len(file)):
        return ("Error Occured when Uploaded All Files to Target Destination: " + str(countOfSuccesses) + " file(s) successfully uploaded ")
