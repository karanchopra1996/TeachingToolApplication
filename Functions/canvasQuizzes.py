import csv

import Functions.canvasFunctions as canvasFunctions
from core.canvas_services import canvas_services as canvasCore

#----------------------------------------------------------------------------
#Function that manages which function to call and returns response to app.py
def QuizManager(courseID, quizID):
    if quizID == None:
        return quizList(courseID)
    return exportQuizSubmissions(courseID, quizID)
#----------------------------------------------------------------------------
#Function exports all student submissions for a specific quiz as a .csv
def exportQuizSubmissions(courseID, quizID):
    response = canvasCore.canvasQuizSubmissions(courseID, quizID)
    if response == "Error":
        return "Error retrieving Quiz submissions."
    submissionList = response.json().get('quiz_submissions')
        
    quizName = canvasCore.getQuizName(courseID, quizID)
    if quizName == "Error":
        return "Error at getting Quiz Name"
    fileName = quizName + ".csv"
    with open(fileName, 'w') as csvFile:
        filewriter = csv.writer(csvFile, delimiter = ',', quotechar = '|', 
        quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(['User ID', 'User Score', 'Number of Attempts',
        'Points Possible', 'Time Spent', 'Preview Submission'])

        for submission in submissionList:
            userName = canvasCore.getStudentName(submission.get('user_id'))
            if response == "Error":
                return "Error retrieving user's name"
            filewriter.writerow([userName, submission.get('score'), submission.get('attempt'), 
                    submission.get('quiz_points_possible'), submission.get('time_spent'), submission.get('html_url')])

    return ("Successfully downloaded all submissions for quiz: " + quizName)
#----------------------------------------------------------------------------
# Returns a list of all quizzes in the course as a .csv
def quizList(courseID):
    quizList = canvasFunctions.getQuiz(courseID)
    if(quizList == "Error"):
        return ("There was an error downloading the quizzes.")

    # Writing the information to a csv file
    with open('Quizzes.csv', 'w') as csvfile:
        filewriter = csv.writer(
            csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(['Quiz Name', 'Quiz ID',
                            'Preview Quiz', 'Number of Attempts', 'Number of Questions', 'Points Possible'])
    
        for quiz in quizList:
            filewriter.writerow([quiz.get('title'), quiz.get('id'), quiz.get('html_url'),
                quiz.get('allowed_attempts'), quiz.get('question_count'), quiz.get('points_possible')])
            
    return ("Successfully downloaded quizzes.")
#------------------------------------------------------------------------------------------------
#Function to import the quiz into QTI format
  
#--------------------------------------------------------------------------------------------------
#Function to export the quiz into QTI format  