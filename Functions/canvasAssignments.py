import csv
import Functions.canvasFunctions as canvasFunctions
from core.canvas_services import canvas_services as canvasCore

#----------------------------------------------------------------------------
# File manager to direct to the right function. Returns response to app.py
def assignmentManager(courseID, assignmentID):
    if(assignmentID == None):
        return assignmentList(courseID)
    return exportAssignmentSubmissions(courseID, assignmentID)
#----------------------------------------------------------------------------
# Function to remove html components of the description
def getDescription(rawDescription):
    cleanedDescription = rawDescription.replace("<p>", "")
    cleanedDescription = cleanedDescription.replace("</p>", "")
    return cleanedDescription
#----------------------------------------------------------------------------
#Function to export the student submissions for a specific assignment as .csv
def exportAssignmentSubmissions(courseID, assignmentID):
    response = canvasCore.canvasAssignmentSubmissions(courseID, assignmentID)
    if response == "Error":
        return "Error at getting Submissions."
    submissionList = response.json()
    
    assignmentName = canvasCore.getAssignmentName(courseID, assignmentID)
    if assignmentName == "Error":
        return "Error at getting Assignment Name"
    fileName = assignmentName + ".csv"
    with open(fileName, 'w') as csvFile:
        filewriter = csv.writer(csvFile, delimiter = ',', quotechar = '|', 
        quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(['User Name', 'Submission Timestamp', 'Number of Attempts',
        'Missing', 'Late', 'Preview Submission'])
    
        for submission in submissionList:
            userName = canvasCore.getStudentName(submission.get('user_id'))
            if response == "Error":
                return "Error retrieving user's name"
            filewriter.writerow([userName, submission.get('submitted_at'), submission.get('attempt'), submission.get('missing'), submission.get('late'), submission.get('preview_url')])    
    return ("Successfully downloaded all submissions for assignment: " + assignmentName)
#----------------------------------------------------------------------------
#Function to export all assignments in a course as a .csv
def assignmentList(courseID):
    assignmentList = canvasFunctions.getAssignment(courseID)
    if(assignmentList == "There was an error finding the course."):
        return ("There was an error finding the course.")    

    # Writing the information to a csv file
    with open('Assignments.csv', 'w') as csvfile:
        filewriter = csv.writer(
            csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(['Assignment Name', 'Assignment ID',
                            'Assignment Group ID', 'Points Available', 'Assignment Description'])
        for assignment in assignmentList:
            filewriter.writerow([assignment.get("name"), assignment.get('id'), assignment.get('assignment_group_id'), assignment.get("points_possible"), getDescription(
                assignment.get("description"))])
    return ("Successfully downloaded all assignments.")
