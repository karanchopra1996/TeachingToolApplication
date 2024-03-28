from .canvas_object import CanvasObject
from .upload import FileOrPathLike, Uploader
from .util import combine_kwargs
from werkzeug.utils import secure_filename
import json
import os

class Submission(CanvasObject):

   def edit(self, course_id, assignment_id, user_id, **kwargs):
      """
      Comment on and/or update the grading for a student's assignment submission.

      :calls: `PUT /api/v1/courses/:course_id/assignments/:assignment_id/submissions/:user_id \
      <https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.update>`_

      :rtype: dict
      """
      response = self._requester.request(
         "PUT",
         "courses/{}/assignments/{}/submissions/{}".format(
               course_id, assignment_id, user_id
         ),
         _kwargs=combine_kwargs(**kwargs),
      )
      response_json = response.json()

      response_json.update(course_id=course_id)

      return response_json

   def mark_read(self, course_id, assignment_id, user_id, **kwargs):
      """
      Mark submission as read. No request fields are necessary.

      :calls: `PUT
         /api/v1/courses/:course_id/assignments/:assignment_id/submissions/:user_id/read \
         <https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.mark_submission_read>`_

      :returns: True if successfully marked as read.
      :rtype: bool
      """
      response = self._requester.request(
         "PUT",
         "courses/{}/assignments/{}/submissions/{}/read".format(
               course_id, assignment_id, user_id
         ),
      )
      return response.status_code == 204

   def mark_unread(self, course_id, assignment_id, user_id, **kwargs):
      """
      Mark submission as unread. No request fields are necessary.

      :calls: `DELETE
         /api/v1/courses/:course_id/assignments/:assignment_id/submissions/:user_id/read \
         <https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.mark_submission_unread>`_

      :returns: True if successfully marked as unread.
      :rtype: bool
      """
      response = self._requester.request(
         "DELETE",
         "courses/{}/assignments/{}/submissions/{}/read".format(
               course_id, assignment_id, user_id
         ),
      )
      return response.status_code == 204

   def upload_comment(self, course_id, assignment_id, user_id, file: FileOrPathLike, **kwargs):
      """
      Upload a file to attach to this submission as a comment.

      :calls: `POST \
      /api/v1/courses/:course_id/assignments/:assignment_id/submissions/:user_id/comments/files \
      <https://canvas.instructure.com/doc/api/submission_comments.html#method.submission_comments_api.create_file>`_

      :param file: The file or path of the file to upload.
      :type file: file or str
      :returns: True if the file uploaded successfully, False otherwise, \
         and the JSON response from the API.
      :rtype: tuple
      """
      response = Uploader(
         self._requester,
         "courses/{}/assignments/{}/submissions/{}/comments/files".format(
               course_id, assignment_id, user_id
         ),
         file,
         **kwargs
      ).start()

      if response[0]:
         self.edit(comment={"file_ids": [response[1]["id"]]})
      return response
   
   # ------------------------------------------------------------------------------
   ### Author: by Pooja Pal 
   # ------------------------------------------------------------------------------
   def uploadSubmissionFiles(self,request,file, **kwargs):
      """
      In order to submit an attached files as part of submission, we need to first upload them to local canvas storage so that it gives a file id. 
      FileId is used in assignmnet submission API
      :param request: request from the UI which has courseId and Assignment Id and other details
      :type request: JSON 
      :param file: file that needs to uploaded
      :param kwargs: keyword arguments if passed any
      :type kwargs: dict 
      :returns: fileId of the file that is successfully uploaded in canvas local storage
      :rtype: HttpResponse having the Fileid
      """
      filename = secure_filename(request.form.get('name'))
      destination="/".join([filename])
      file.save(destination)
      studentId = request.form.get('studentId')    
      data = json.dumps({'name': filename,
                        'size': request.form.get('size'),
                        'content-type': request.form.get('content_type')})
      files = {"file": open(filename, 'rb')}
      url = "/users/" + studentId + "/files"
      response = self._requester.getFileId(url, data, files)
      os.remove(filename)
      return response
   
   def submitAnAssignment(self,request, **kwargs):
      """
      Makes use of the file id from the requests and submits them to the canvas submission section
      :calls: `POST 
      :param request: request with file id, submission details
      :type request: JSON 
      :returns: submission response
      :rtype: HttpResponse
      """
      print(" request got =>", request)
      data = {
               "submission" :
               {
                     "user_id":str(request['submitterData']['id']),
                     "submission_type":request['submission_type'],
                     "body":request['submission_body'],
                     "file_ids": request['fileIds']
               },
               "comment" :
                     {
                        "text_comment":request['comment']
                     }
            }  
      endpoint = "courses/{}/assignments/{}/submissions".format(str(request['courseId']),str(request['assignId']))
      response = self._requester.submitAssignments(
         endpoint,
         data)
      print(" response =.", response.status_code)
      return response
   
   # ----------------------Helper function to submission API--------------------------------------------------------                
   def updateCommentsForContributors(self,request,**kwargs):
      """ Submitter and group details gets published as part of comments. This method broadcasts the comments to the all the group members
      :param request: The request from the UI 
      :type request: JSON 
      :returns: None
      :rtype: None
      """
      try:
         print(" in update comments ")
         contributors = request['contributors']
         print(" contributors =>", contributors)
         for contributor in contributors:
            
            endpoint = "courses/{}/assignments/{}/submissions/{}".format(str(request['courseId']), str(request['assignId']), str(contributor.get('id')))
            token = '10~SdVWOO1ZQTXKNs43iOhgs9Mj1cZgtmq1V5xcgmG42mxpdg5o7ysgyvUYbsmpkiVT'  
            header = {"Authorization": "Bearer {}".format(token)}
            data = { 'comment[text_comment]': request['comment']}
            kwargs.update(data)
            updateComments = self._requester.request( "PUT",
                                                endpoint,
                                                use_auth = False,
                                                headers = header,
                                                **kwargs)  
            print(" update status =>",updateComments.status_code )   
         return updateComments
      except Exception as e :
         print(" Exception occured during updation", e)  
         
   def getContributorDetails(self,contributors):
      """ 
      Submitter and group details gets published as part of comments. This method fetches team member names and their student Ids
      :param contributors: list having studentid and student name
      :type contributors: List 
      :returns: Members data - students details
      :rtype: List
      """
      membersData = []
      for studentId in contributors:
         print(" contributor",studentId)
         endpoint = "users/{}/profile".format(str(studentId))
         print(" endpoint =>", endpoint)
               #never store tokens in the code, To be removed
         token = '10~SdVWOO1ZQTXKNs43iOhgs9Mj1cZgtmq1V5xcgmG42mxpdg5o7ysgyvUYbsmpkiVT'  
         header = {"Authorization": "Bearer {}".format(token)}
         response = self._requester.request( 
                                                "GET",
                                                endpoint, 
                                                use_auth = False,
                                                headers = header)
         if response.status_code != 200:
            return json.loads(response.text)
         else:
            membersData.append([response.json()['name'],response.json()['id'], response.json()['login_id'], "contributor"])
      return membersData
   
   def getSubmissions(self, request,**kwargs):
      # endpoint = "/courses/{}/assignments/{}/submissions".format(str(request['courseId']), str(request['assignId']))
      # print(" endpoint =>>>>>>>>", endpoint)
      # params = { 'include[]':['submission_comments', 'user']}
      # groupInfo = self._requester.getWithParams(endpoint,  params)
      # return groupInfo
      """ 
      get all the assignment submissions for particular course and assignment combination
      :param request: UI request having course and assignment ids
      :type request: JSON 
      :returns: submission object
      :rtype: HttpResponse
      """
      endpoint = "/courses/{}/assignments/{}/submissions".format(str(request['courseId']), str(request['assignId']))
      kwargs['include'] = ['submission_comments','user']
      response = self._requester.request(
         "GET",
         endpoint,
         _kwargs=combine_kwargs(**kwargs)
      )
      return response

  

          
