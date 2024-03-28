from __future__ import print_function
import wget

import os.path
import os
import threading

import Functions.canvasFunctions as canvasFunctions
import Functions.googleFunctions as googleFunctions
#-------------------------------------------------------------------------------

def downloadSyllabus(courseID, files, downloadToLocal=True):
    fileURL = findSyllabus(files)
    if fileURL is None:
        return ("File not found")
    status = downloadFile(fileURL)
    # status = upload(courseID, files, downloadToLocal)
    # if downloadToLocal == True:
    #     return ("Uploaded Syllabus file to Google Drive and saved to your Local machine.")
    # else:
    #     return ("Uploaded Syllabus file to Google Drive.")
    return status

def downloadFile(fileURL):
    wget.download(fileURL)
    return ("Download was successful")

def findSyllabus(files):
    for file in files:
        fileName = file.get('display_name')
        if "syllabus" in fileName.lower():
            return file.get('url')
    return None
#-------------------------------------------------------------------------------
#Function manager to call upload function and then return response to app.py
# def downloadSyllabus(courseID, downloadToLocal):
#         courseName = canvasFunctions.courseName(courseID)
#         files = canvasFunctions.getAllFiles(courseID)
#         if(files == "Error"):
#             return ("Error")
#         status = upload(courseID, courseName, files, downloadToLocal)
#         if(status == "Error"):
#             return ("There was an error finding the course.")

#         if downloadToLocal == True:
#             return ("Uploaded Syllabus file to Google Drive and saved to your Local machine.")
#         else:
#             return ("Uploaded Syllabus file to Google Drive.")

# Method checks to see if the file contains the word 'Syllabus' in it to ensure we are downloading the proper file
def isSyllabus(file):
    if "syllabus" in file.lower():
        return True
    elif "Syllabus" in file:
        return True
    else:
        return False
#-------------------------------------------------------------------------------
# Function to extract the syllabus file from the Canvas Api in the specified course
# If downloadToLocal is true then the file will be saved on the users local machine
def upload(courseID, files, downloadToLocal):

    downloadableFileURL = None
    for file in files:
        fileName = file.get("display_name")
        if isSyllabus(fileName) == True:
            downloadableFileURL = file.get("url")
            break

    wget.download(downloadableFileURL)
    updatedFileName = fileName
    os.rename(fileName, updatedFileName)

    thread = threading.Thread(
        googleFunctions.uploadToDrive((updatedFileName)))
    thread.start()
    thread.join()
    if downloadToLocal == False:
        os.remove(updatedFileName)
    return ("Download was successful")


