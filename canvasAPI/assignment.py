from .canvas_object import CanvasObject
from .exceptions import RequiredFieldMissing, CanvasException
from .paginated_list import PaginatedList
from .upload import FileOrPathLike, Uploader
from .util import combine_kwargs

class Assignment(CanvasObject):

   def get_submission(self, course_id, assignment_id, user_id, **kwargs):
      """
      Get a single submission, based on user id.
      :calls: `GET /api/v1/courses/:course_id/assignments/:assignment_id/submissions/:user_id \
      <https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.show>`_
      :rtype: dict
      """

      response = self._requester.request(
         "GET",
         "courses/{}/assignments/{}/submissions/{}".format(
               course_id, assignment_id, user_id
         ),
         _kwargs=combine_kwargs(**kwargs),
      )
      response_json = response.json()
      response_json.update(course_id=course_id)

      return response_json

   def get_submissions(self, course_id, assignment_id, **kwargs):
      """
      Get all existing submissions for this assignment.
      :calls: `GET /api/v1/courses/:course_id/assignments/:assignment_id/submissions  \
      <https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.index>`_
      :rtype: :class:`canvasapi.paginated_list.PaginatedList`
      """
      return PaginatedList(
         self._requester,
         "GET",
         "courses/{}/assignments/{}/submissions".format(course_id, assignment_id),
         {"course_id": course_id},
         _kwargs=combine_kwargs(**kwargs),
      )

   def create_override(self, course_id, assignment_id, **kwargs):
      """
      Create an override for this assignment.
      :calls: `POST /api/v1/courses/:course_id/assignments/:assignment_id/overrides \
      <https://canvas.instructure.com/doc/api/assignments.html#method.assignment_overrides.create>`_
      :rtype: dict
      """
      response = self._requester.request(
         "POST",
         "courses/{}/assignments/{}/overrides".format(course_id, assignment_id),
         _kwargs=combine_kwargs(**kwargs),
      )
      response_json = response.json()
      response_json.update(course_id=course_id)
      return response_json

   def delete(self, course_id, assignment_id, **kwargs):
      """
      Delete this assignment.
      :calls: `DELETE /api/v1/courses/:course_id/assignments/:id \
      <https://canvas.instructure.com/doc/api/assignments.html#method.assignments.destroy>`_
      :rtype: dict
      """
      response = self._requester.request(
         "DELETE",
         "courses/{}/assignments/{}".format(course_id, assignment_id),
         _kwargs=combine_kwargs(**kwargs),
      )
      return response.json()

   def edit(self, course_id, assignment_id, **kwargs):
      """
      Modify this assignment.
      :calls: `PUT /api/v1/courses/:course_id/assignments/:id \
      <https://canvas.instructure.com/doc/api/assignments.html#method.assignments_api.update>`_
      :rtype: dict
      """
      response = self._requester.request(
         "PUT",
         "courses/{}/assignments/{}".format(course_id, assignment_id),
         _kwargs=combine_kwargs(**kwargs),
      )
      return response.json()

   def get_gradeable_students(self, course_id, assignment_id, **kwargs):
      """
      List students eligible to submit the assignment.
      :calls: `GET /api/v1/courses/:course_id/assignments/:assignment_id/gradeable_students  \
      <https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.gradeable_students>`_
      :rtype: :class:`canvasapi.paginated_list.PaginatedList` of
         :class:`canvasapi.user.UserDisplay`
      """
      return PaginatedList(
         self._requester,
         "GET",
         "courses/{}/assignments/{}/gradeable_students".format(
               course_id, assignment_id
         ),
         {"course_id": course_id},
         _kwargs=combine_kwargs(**kwargs),
      )

   def get_override(self, course_id, assignment_id, override_id, **kwargs):
      """
      Get a single assignment override with the given override id.
      :calls: `GET /api/v1/courses/:course_id/assignments/:assignment_id/overrides/:id \
      <https://canvas.instructure.com/doc/api/assignments.html#method.assignment_overrides.show>`_
      :rtype: dict
      """

      response = self._requester.request(
         "GET",
         "courses/{}/assignments/{}/overrides/{}".format(
               course_id, assignment_id, override_id
         ),
         _kwargs=combine_kwargs(**kwargs),
      )
      response_json = response.json()
      response_json.update(course_id=course_id)
      return response_json

   def get_overrides(self, course_id, assignment_id, **kwargs):
      """
      Get a paginated list of overrides for this assignment that target
      sections/groups/students visible to the current user.
      :calls: `GET /api/v1/courses/:course_id/assignments/:assignment_id/overrides \
      <https://canvas.instructure.com/doc/api/assignments.html#method.assignment_overrides.index>`_
      :rtype: :class:`canvasapi.paginated_list.PaginatedList`
      """
      return PaginatedList(
         self._requester,
         "GET",
         "courses/{}/assignments/{}/overrides".format(course_id, assignment_id),
         {"course_id": course_id},
         _kwargs=combine_kwargs(**kwargs),
      )

   def get_peer_reviews(self, course_id, assignment_id, **kwargs):
      """
      Get a list of all Peer Reviews for this assignment.
      :calls: `GET /api/v1/courses/:course_id/assignments/:assignment_id/peer_reviews \
      <https://canvas.instructure.com/doc/api/peer_reviews.html#method.peer_reviews_api.index>`_
      :rtype: :class:`canvasapi.paginated_list.PaginatedList`
      """
      return PaginatedList(
         self._requester,
         "GET",
         "courses/{}/assignments/{}/peer_reviews".format(course_id, assignment_id),
         _kwargs=combine_kwargs(**kwargs),
      )

   def set_extensions(self, course_id, assignment_id, assignment_extensions, **kwargs):
      """
      Set extensions for student assignment submissions
      :calls: `POST /api/v1/courses/:course_id/assignments/:assignment_id/extensions \
      <https://canvas.instructure.com/doc/api/assignment_extensions.html#method.assignment_extensions.create>`_
      :param assignment_extensions: list of dictionaries representing extensions
      :type assignment_extensions: list
      :rtype: list of dictionaries
      Example Usage:
      >>> assignment.set_extensions([
      ...     {
      ...         'user_id': 3,
      ...         'extra_attempts': 2
      ...     },
      ...     {
      ...         'user_id': 2,
      ...         'extra_attempts': 2
      ...     }
      ... ])
      """
      if not isinstance(assignment_extensions, list) or not assignment_extensions:
         raise ValueError("Param `assignment_extensions` must be a non-empty list.")

      if any(not isinstance(extension, dict) for extension in assignment_extensions):
         raise ValueError(
               "Param `assignment_extensions` must only contain dictionaries"
         )

      if any("user_id" not in extension for extension in assignment_extensions):
         raise RequiredFieldMissing(
               "Dictionaries in `assignment_extensions` must contain key `user_id`"
         )
      kwargs["assignment_extensions"] = assignment_extensions
      response = self._requester.request(
         "POST",
         "courses/{}/assignments/{}/extensions".format(course_id, assignment_id),
         _kwargs=combine_kwargs(**kwargs),
      )
      extension_list = response.json()["assignment_extensions"]
      return extension_list

   def delete_assignment_group(self, course_id, assignment_group_id, **kwargs):
      """
      Delete this assignment.
      :calls: `DELETE /api/v1/courses/:course_id/assignment_groups/:assignment_group_id \
      <https://canvas.instructure.com/doc/api/assignment_groups.html#method.assignment_groups_api.destroy>`_
      :rtype: dict
      """
      response = self._requester.request(
         "DELETE",
         "courses/{}/assignment_groups/{}".format(course_id, assignment_group_id),
         _kwargs=combine_kwargs(**kwargs),
      )
      return response.json()

   def edit_assignment_group(self, course_id, assignment_group_id, **kwargs):
      """
      Modify this assignment group.
      :calls: `PUT /api/v1/courses/:course_id/assignment_groups/:assignment_group_id \
      <https://canvas.instructure.com/doc/api/assignment_groups.html#method.assignment_groups_api.update>`_
      :rtype: dict
      """
      response = self._requester.request(
         "PUT",
         "courses/{}/assignment_groups/{}".format(course_id, assignment_group_id),
         _kwargs=combine_kwargs(**kwargs),
      )
      return response.json()

   def delete_override(self, course_id, assignment_id, override_id, **kwargs):
      """
      Delete this assignment override.
      :calls: `DELETE /api/v1/courses/:course_id/assignments/:assignment_id/overrides/:id
      <https://canvas.instructure.com/doc/api/assignments.html#method.assignment_overrides.destroy>`_
      :returns: The previous content of the now-deleted assignment override.
      :rtype: dict
      """
      response = self._requester.request(
         "DELETE",
         "courses/{}/assignments/{}/overrides/{}".format(
               course_id, assignment_id, override_id
         ),
         _kwargs=combine_kwargs(**kwargs),
      )

      response_json = response.json()
      response_json.update(course_id=course_id)

      return response_json

   def edit_override(self, course_id, assignment_id, override_id, **kwargs):
      """
      Update this assignment override.
      Note: All current overridden values must be supplied if they are to be retained.
      :calls: `PUT /api/v1/courses/:course_id/assignments/:assignment_id/overrides/:id
      <https://canvas.instructure.com/doc/api/assignments.html#method.assignment_overrides.update>`_
      :rtype: dict
      """
      response = self._requester.request(
         "PUT",
         "courses/{}/assignments/{}/overrides/{}".format(
               course_id, assignment_id, override_id
         ),
         _kwargs=combine_kwargs(**kwargs),
      )

      response_json = response.json()
      response_json.update(course_id=course_id)
      return response_json

   def upload_to_submission(self, course_id, assignment_id, file: FileOrPathLike, user_id="self", **kwargs):
      """
      Upload a file to a submission.
      :calls: `POST /api/v1/courses/:course_id/assignments/:assignment_id/ \
         submissions/:user_id/files \
      <https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.create_file>`_
      :param file: The file or path of the file to upload.
      :type file: FileLike
      :param user: The ID of the related user, or 'self' for the
         current user. Defaults to 'self'.
      :type user:int, or str
      :returns: True if the file uploaded successfully, False otherwise, \
                  and the JSON response from the API.
      :rtype: tuple
      """

      return Uploader(
         self._requester,
         "courses/{}/assignments/{}/submissions/{}/files".format(
               course_id, assignment_id, user_id
         ),
         file,
         **kwargs
      ).start()
   
   def submit(self, course_id, assignment_id, submission, file=None, **kwargs):
      """
      Makes a submission for an assignment.
      :calls: `POST /api/v1/courses/:course_id/assignments/:assignment_id/submissions \
      <https://canvas.instructure.com/doc/api/submissions.html#method.submissions.create>`_
      :param submission: The attributes of the submission.
      :type submission: dict
      :param file: A file to upload with the submission. (Optional,
         defaults to `None`. Submission type must be `online_upload`)
      :type file: file or str
      :rtype: dict
      """
      if isinstance(submission, dict) and "submission_type" in submission:
         kwargs["submission"] = submission
      else:
         raise RequiredFieldMissing(
               "Dictionary with key 'submission_type' is required."
         )

      if file:
         if submission.get("submission_type") != "online_upload":
               raise ValueError(
                  "To upload a file, `submission['submission_type']` must be `online_upload`."
               )

         upload_response = self.upload_to_submission(course_id, assignment_id, file, **kwargs)
         if upload_response[0]:
               kwargs["submission"]["file_ids"] = [upload_response[1]["id"]]
         else:
               raise CanvasException("File upload failed. Not submitting.")

      response = self._requester.request(
         "POST",
         "courses/{}/assignments/{}/submissions".format(course_id, assignment_id),
         _kwargs=combine_kwargs(**kwargs),
      )
      response_json = response.json()
      response_json.update(course_id=course_id)

      return response_json
   
   #---------------------------------------------------------------------------------------------
   #Author: Pooja Pal
   #---------------------------------------------------------------------------------------------
   def getAssignmentMetadata(self, request, **kwargs):
      """
      Fetches metadata about the assignmnets such as number of attempts, type of acceptable files
      :param request: The request object from the UI from which course Id and assignment Ids are parsed
      :type request: Json
      :rtype: Http Response object
      """
      courseId = str(request['courseId'])
      assignId = str(request['assignId']) 
      response = self._requester.request(
         "GET",
         "courses/{}/assignments/{}".format(courseId, assignId),
         _kwargs=combine_kwargs(**kwargs),
      )
      return response
   
   def getSubmitterData(self,**kwargs):
      """
      The currently logged in user acts as a submitter for any assignment that is submitted by its account. The submitter data include name, id and other details
      :rtype: Http Response object 
      """
      response = self._requester.request(
      "GET",
      "/users/self/",
      _kwargs=combine_kwargs(**kwargs),
      )
      return response
   
   def getAssignmentName(self,request):
      """
      Fetches assignment name for the given course and assignment Id combination
      :param request: The request object from the UI from which course Id and assignment Ids are parsed
      :type request: Json
      :rtype: Http Response object 
      """
      endpoint = "/courses/{}/assignments/{}".format(str(request['courseId']), str(request['assignId']))
      assignment = self._requester.request("GET", endpoint)  
      return  assignment
   
   def listAssignmnets(self, courseId, **kwargs):
      """
      Fetches assignment name for the given course and assignment Id combination
      :param courseId: The course Id from from the UI request object
      :type courseId: string
      :param kwargs: The list of keyword arguments that can be passed from the calling function 
      :type kwargs: dict
      :rtype: Http Response object 
      """
      endpoint = "courses/{}/assignments".format(courseId)
      kwargs['per_page'] = 50
      response = self._requester.request(
         "GET",
         endpoint,
         _kwargs=combine_kwargs(**kwargs)
      )
      return response
          
          
      