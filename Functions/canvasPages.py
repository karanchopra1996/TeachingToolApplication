import pypandoc
import os
import threading
import Functions.googleFileContents as gFileContents
import Functions.canvasFunctions as canvasFunctions
import Functions.googleFunctions as googleFunctions

#----------------------------------------------------------------------------
# Function to return the HTML and content of the specific canvas page as a html page(canvasPage.html)
def getFileContent(id, canvasPage):
    courseID = str(id)
    pageResponse = canvasFunctions.getCanvasPage(courseID, canvasPage)
    if(pageResponse == "There was an error finding the course."):
        return ("There was an error finding the course.")
    dirtyString = pageResponse.get('body')
    fileName = pageResponse.get('title')
    f = open("canvasPage.html", "x")
    f.write(dirtyString)
    f.close()

    pypandoc.convert_file('canvasPage.html', 'docx',
                            outputfile=(fileName + ".docx"))

    os.remove("canvasPage.html")
    
    return fileName
#----------------------------------------------------------------------------
# Function to create page and publish it to canvas
def createPage(courseID, googleFileTitle, googleFileContent):
    canvasFunctions.createCanvasPage(
        courseID, googleFileTitle, googleFileContent)
#----------------------------------------------------------------------------
# Function will download file from google drive and upload to Canvas Pages
def downloadFromDriveToCanvasPage(courseID, googleFileID, googleFile):
    index = googleFile.index('_')
    googleFile = googleFile[0:index]
    status = googleFileContents = gFileContents.getFileContents(
        googleFileID)
    if status == "Error":
        return "There was an error finding the google file."
    createPage(courseID, googleFile, googleFileContents)
    return ("Successfully created canvas page from google drive file")
#----------------------------------------------------------------------------
# Function will download Canvas Page and upload to a file in Google Drive
def downloadPageToDrive(courseID, canvasPageName):
    fileName = getFileContent(courseID, canvasPageName)
    if fileName == "There was an error finding the course.":
        return ("There was an error finding the course.")
    thread = threading.Thread(
        googleFunctions.uploadToDrive((fileName+".docx")))
    thread.start()
    thread.join()
    os.remove((fileName+".docx"))
    return ("Successfully exported canvas page and imported it to google drive")