from .canvas_object import CanvasObject
import mysql.connector
import json
from mysql.connector import Error

# DB connection
f = open("/Users/karanc4/teaching-tools/canvasAPI/db_credentials.json")
credentials = json.load(f)
f.close()

class Database(CanvasObject):
    """
    The database class gets the credentials from the `db_credentials.json` and performs crud operations
   """
    def update_submission_in_db(self, request, submission_response):
        """
        After the assignments is submitted this method stores the submission related collaborators information 
        param request: The UI request that has course related information
        param type : JSON
        param submission_response: response body after asn assignment submission 
        type submission_response: JSON
        returns success or error string
        """
        try:
            connection = mysql.connector.connect(host = credentials['host'],
                                                database = credentials['database'],
                                                user = credentials['user'],
                                                password= credentials['password'])
            studentList = []
            for student in request['contributors']:
                studentList.append(student['id'])
                
            if connection.is_connected():
                db_Info = connection.get_server_info()
                print("Connected to MySQL Server version ", db_Info)
                submissionId = submission_response['id']
                select_query =  """ SELECT * from assignment_submitters 
                                    where submission_id = %s """
                cursor = connection.cursor()
                cursor.execute(select_query,(submissionId,))
                cursor.fetchall()
                
                if cursor.rowcount < 1:
                    """ insert if the records are not available"""
                    insertQuery = "INSERT INTO assignment_submitters (submission_id,course_id,assignment_id,submitter_canvas_id ,submitter_name,submitter_login_id,submission_status,contributors) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                    values = (str(submission_response['id']), request['courseId'],request['assignId'], request['submitterData']['id'],request['submitterData']['name'],request['submitterData']['short_name'],submission_response['workflow_state'],str(studentList)  )
                    
                    cursor.execute(insertQuery, values)
                    connection.commit()
                    return "success"
                else:
                    """ update record with the another submission is submitted """
                    contributors = (str(request['contributors']))
                    cursor.execute ("""
                    UPDATE assignment_submitters
                    SET contributors=%s 
                    WHERE submission_id=%s
                    """, (str(studentList), submissionId))
                    connection.commit()
                    return "success"
        except Error as e:
            print("Error while connecting to MySQL", e)
            return "error"
        finally:
            if connection.is_connected():
                connection.close()
                print("MySQL connection is closed")
                
    def get_contributors_from_db(self,submission_id):
        """
        UI request that has course related information
        param type : JSON
        param submission_Id: Id of teh submission for which the collaborators needs to be extracted
        type submission_response: JSON
        returns success or error string
        """
        try:
            connection = mysql.connector.connect(host = credentials['host'],
                                                database = credentials['database'],
                                                user = credentials['user'],
                                                password= credentials['password'])
            if connection.is_connected():
                db_Info = connection.get_server_info()
                print("Connected to MySQL Server version ", db_Info)
                select_query =  """ SELECT contributors from assignment_submitters 
                                    where submission_id = %s """
                cursor = connection.cursor()
                cursor.execute(select_query,(submission_id,))
                records = list(cursor.fetchall())
                for row in records:
                    trimmed_row = row[0][1:-1]
                    contributors = trimmed_row.split(",")
                    return contributors
                return []
        except Error as e:
            print("Error while connecting to MySQL", e)
            return "error"
        finally:
            if connection.is_connected():
                connection.close()
                print("MySQL connection is closed")