import csv
import re

CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')

def cleanhtml(raw_html):
   """ remove all html entities using regex """
   cleantext = re.sub(CLEANR, '', raw_html)
   return cleantext
#----------------------------------------------------------------------------
# Function to remove html components of the description
def getDescription(rawDescription):
   """ remove html components of the description and return only the first line
   """
   try:
      cleanedDescription = rawDescription.splitlines()[0]
   except:
      cleanedDescription = rawDescription

   cleanedDescription = cleanhtml(cleanedDescription)
   return cleanedDescription

#----------------------------------------------------------------------------
#Function to export all assignments in a course as a .csv
def assignmentListCSV(assignments):
   """ exports a list of all assignments in the course as a .csv
   """
   fileName = 'Assignments.csv'
   headers = ['Assignment Name', 
               'Assignment ID', 
               'Assignment Group ID', 
               'Points Available', 
               'Assignment Description']
   
   with open(fileName, 'w', newline='') as csvfile:
      filewriter = csv.writer(
            csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
      filewriter.writerow(headers)

      for assignment in assignments:
         filewriter.writerow([assignment.get("name"), 
                              assignment.get('id'), 
                              assignment.get('assignment_group_id'), 
                              assignment.get("points_possible"), 
                              getDescription(assignment.get("description"))])
   return ("Successfully downloaded all assignments.")

#----------------------------------------------------------------------------
def exportSubmissions(course, assignment):
   """ Exports all student submissions for a specified assignment as a .csv file 
   """
   assignmentName = assignment.name
   fileName = '{}.csv'.format(assignmentName)
   headers = ['User Name', 
               'Submission Timestamp', 
               'Number of Attempts',
               'Missing', 
               'Late', 
               'Preview Submission']

   with open(fileName, 'w', newline='') as csvFile:
      filewriter = csv.writer(
         csvFile, delimiter = ',', quotechar = '|', quoting=csv.QUOTE_MINIMAL)
      filewriter.writerow(headers)

      for submission in assignment.submissions:
         userID = submission.get('user_id')
         user = course.getUserById(userID)
         if user is None:
            userName = 'Test Student'
         else:
            userName = user.name

         filewriter.writerow([userName, 
                              submission.get('submitted_at'), 
                              submission.get('attempt'), 
                              submission.get('missing'), 
                              submission.get('late'), 
                              submission.get('preview_url')])
   
   return ("Successfully downloaded all submissions for assignment: " + assignmentName)