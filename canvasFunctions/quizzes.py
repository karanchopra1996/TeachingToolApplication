import csv

#----------------------------------------------------------------------------
def quizListCSV(quizzes):
   """ exports a list of all quizzes in the course as a .csv
   """
   fileName = 'Quizzes.csv'
   headers = ['Quiz Name', 
               'Quiz ID',
               'Preview Quiz', 
               'Number of Attempts',
               'Number of Questions', 
               'Points Possible']
   
   # Writing the information to a csv file
   with open(fileName, 'w', newline='') as csvfile:
      filewriter = csv.writer(
            csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
      filewriter.writerow(headers)
   
      for quiz in quizzes:
         filewriter.writerow([quiz.get('title'), 
                              quiz.get('id'), 
                              quiz.get('html_url'), 
                              quiz.get('allowed_attempts'), 
                              quiz.get('question_count'), 
                              quiz.get('points_possible')])            
   return ("Successfully downloaded quizzes.")

#----------------------------------------------------------------------------
def exportQuizSubmissions(course, quiz):
   """ Exports all student submissions for a specified quiz as a .csv file 
   """
   fileName = quiz.title + '.csv'
   headers = ['User ID',
               'User Name'
               'User Score', 
               'Number of Attempts',
               'Points Possible', 
               'Time Spent', 
               'Preview Submission']

   with open(fileName, 'w', newline='') as csvFile:
      filewriter = csv.writer(
            csvFile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
      filewriter.writerow(headers)
      
      for submission in quiz.submissions:
            userID = submission.get('user_id')
            user = course.getUserById(userID)
            if user is None:
               userName = 'Test Student'
            else:
               userName = user.name
            
            filewriter.writerow([userID,
                              userName,
                              submission.get('score'),
                              submission.get('attempt'), 
                              submission.get('quiz_points_possible'), 
                              submission.get('time_spent'), 
                              submission.get('html_url')])
   
   return ("Successfully downloaded all submissions for quiz: " + quiz.title)