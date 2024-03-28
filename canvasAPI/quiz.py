from .canvas_object import CanvasObject
from .exceptions import RequiredFieldMissing
from .paginated_list import PaginatedList
from .util import combine_kwargs


class Quiz(CanvasObject):

   def create_question(self, course_id, quiz_id, **kwargs):
      """
      Create a new quiz question for this quiz.

      :calls: `POST /api/v1/courses/:course_id/quizzes/:quiz_id/questions \
      <https://canvas.instructure.com/doc/api/quiz_questions.html#method.quizzes/quiz_questions.create>`_

      :rtype: dict
      """

      response = self._requester.request(
         "POST",
         "courses/{}/quizzes/{}/questions".format(course_id, quiz_id),
         _kwargs=combine_kwargs(**kwargs),
      )

      response_json = response.json()
      response_json.update({"course_id": course_id})

      return response_json

   def create_report(self, course_id, quiz_id, report_type, **kwargs):
      """
      Create and return a new report for this quiz. If a previously generated report
      matches the arguments and is still current (i.e. there have been no new submissions),
      it will be returned.

      :calls: `POST /api/v1/courses/:course_id/quizzes/:quiz_id/reports \
      <https://canvas.instructure.com/doc/api/quiz_reports.html#method.quizzes/quiz_reports.create>`_

      :param report_type: The type of report, either student_analysis or item_analysis
      :type report_type: str

      :rtype: dict
      """
      if report_type not in ["student_analysis", "item_analysis"]:
         raise ValueError(
               "Param `report_type` must be a either 'student_analysis' or 'item_analysis'"
         )

      kwargs["quiz_report"] = {"report_type": report_type}

      response = self._requester.request(
         "POST",
         "courses/{}/quizzes/{}/reports".format(course_id, quiz_id),
         _kwargs=combine_kwargs(**kwargs),
      )

      response_json = response.json()
      response_json.update({"course_id": course_id})

      return response_json

   def create_submission(self, course_id, quiz_id, **kwargs):
      """
      Start taking a Quiz by creating a QuizSubmission can be used to answer
      questions and submit answers.

      :calls: `POST /api/v1/courses/:course_id/quizzes/:quiz_id/submissions \
      <https://canvas.instructure.com/doc/api/quiz_submissions.html#method.quizzes/quiz_submissions_api.create>`_

      :rtype: dict
      """
      response = self._requester.request(
         "POST",
         "courses/{}/quizzes/{}/submissions".format(course_id, quiz_id),
         _kwargs=combine_kwargs(**kwargs),
      )

      response_json = response.json()["quiz_submissions"][0]
      response_json.update({"course_id": course_id})

      return response_json

   def delete(self, course_id, quiz_id, **kwargs):
      """
      Delete this quiz.

      :calls: `DELETE /api/v1/courses/:course_id/quizzes/:id \
      <https://canvas.instructure.com/doc/api/quizzes.html#method.quizzes/quizzes_api.destroy>`_

      :rtype: dict
      """
      response = self._requester.request(
         "DELETE",
         "courses/{}/quizzes/{}".format(course_id, quiz_id),
         _kwargs=combine_kwargs(**kwargs),
      )
      quiz_json = response.json()
      quiz_json.update({"course_id": course_id})

      return quiz_json

   def edit(self, course_id, quiz_id, **kwargs):
      """
      Modify this quiz.

      :calls: `PUT /api/v1/courses/:course_id/quizzes/:id \
      <https://canvas.instructure.com/doc/api/quizzes.html#method.quizzes/quizzes_api.update>`_

      :returns: The updated quiz.
      :rtype: dict
      """
      response = self._requester.request(
         "PUT",
         "courses/{}/quizzes/{}".format(course_id, quiz_id),
         _kwargs=combine_kwargs(**kwargs),
      )
      quiz_json = response.json()
      quiz_json.update({"course_id": course_id})

      return quiz_json

   def get_all_quiz_reports(self, course_id, quiz_id, **kwargs):
      """
      Get a list of all quiz reports for this quiz

      :calls: `GET /api/v1/courses/:course_id/quizzes/:quiz_id/reports \
      <https://canvas.instructure.com/doc/api/quiz_reports.html#method.quizzes/quiz_reports.index>`_

      :rtype: :class: canvasAPI.paginated_list.PaginatedList'
      """
      return PaginatedList(
         self._requester,
         "GET",
         "courses/{}/quizzes/{}/reports".format(course_id, quiz_id),
         _kwargs=combine_kwargs(**kwargs),
      )

   def get_question(self, course_id, quiz_id, question_id, **kwargs):
      """
      Get as single quiz question by ID.

      :calls: `GET /api/v1/courses/:course_id/quizzes/:quiz_id/questions/:id \
      <https://canvas.instructure.com/doc/api/quiz_questions.html#method.quizzes/quiz_questions.show>`_

      :rtype: dict
      """

      response = self._requester.request(
         "GET",
         "courses/{}/quizzes/{}/questions/{}".format(
               course_id, quiz_id, question_id
         ),
         _kwargs=combine_kwargs(**kwargs),
      )
      response_json = response.json()
      response_json.update({"course_id": course_id})

      return response_json

   def get_questions(self, course_id, quiz_id, **kwargs):
      """
      List all questions for a quiz.

      :calls: `GET /api/v1/courses/:course_id/quizzes/:quiz_id/questions \
      <https://canvas.instructure.com/doc/api/quiz_questions.html#method.quizzes/quiz_questions.index>`_

      :rtype: :class:`canvasAPI.paginated_list.PaginatedList`
      """
      return PaginatedList(
         self._requester,
         "GET",
         "courses/{}/quizzes/{}/questions".format(course_id, quiz_id),
         {"course_id": course_id},
         _kwargs=combine_kwargs(**kwargs),
      )

   def get_quiz_group(self, course_id, quiz_id, quiz_group_id, **kwargs):
      """
      Get details of the quiz group with the given id

      :calls: `GET /api/v1/courses/:course_id/quizzes/:quiz_id/groups/:id \
      <https://canvas.instructure.com/doc/api/quiz_question_groups.html#method.quizzes/quiz_groups.show>`_

      :param id: The ID of the question group.
      :type id: int

      :rtype: dict
      """
      response = self._requester.request(
         "GET",
         "courses/{}/quizzes/{}/groups/{}".format(course_id, quiz_id, quiz_group_id),
         _kwargs=combine_kwargs(**kwargs),
      )

      response_json = response.json()
      response_json.update({"course_id": course_id})

      return response_json

   def get_quiz_report(self, course_id, quiz_id, quiz_report_id, **kwargs):
      """
      Returns the data for a single quiz report.

      :calls: `GET /api/v1/courses/:course_id/quizzes/:quiz_id/reports/:id \
      <https://canvas.instructure.com/doc/api/quiz_reports.html#method.quizzes/quiz_reports.show>`_

      :rtype: dict
      """

      response = self._requester.request(
         "GET",
         "courses/{}/quizzes/{}/reports/{}".format(course_id, quiz_id, quiz_report_id),
         _kwargs=combine_kwargs(**kwargs),
      )

      response_json = response.json()
      response_json.update({"course_id": course_id})

      return response_json

   def get_quiz_submission(self, course_id, quiz_id, quiz_submission_id, **kwargs):
      """
      Get a single quiz submission.

      :calls: `GET /api/v1/courses/:course_id/quizzes/:quiz_id/submissions/:id \
      <https://canvas.instructure.com/doc/api/quiz_submissions.html#method.quizzes/quiz_submissions_api.show>`_

      :rtype: dict
      """
  
      response = self._requester.request(
         "GET",
         "courses/{}/quizzes/{}/submissions/{}".format(
               course_id, quiz_id, quiz_submission_id
         ),
         _kwargs=combine_kwargs(**kwargs),
      )

      response_json = response.json()["quiz_submissions"][0]
      response_json.update({"course_id": course_id})
      if len(response.json().get("quizzes", [])) > 0:
         response_json.update(
               {"quiz": response.json()["quizzes"][0]}
         )
      if len(response.json().get("submissions", [])) > 0:
         response_json.update(
               {"submission": response.json()["submissions"][0]}
         )
      if len(response.json().get("users", [])) > 0:
         response_json.update(
               {"user": response.json()["users"][0]}
         )

      return response_json

   def get_statistics(self, course_id, quiz_id, **kwargs):
      """
      Get statistics for for all quiz versions, or the latest quiz version.

      :calls: `GET /api/v1/courses/:course_id/quizzes/:quiz_id/statistics \
      <https://canvas.instructure.com/doc/api/quiz_statistics.html#method.quizzes/quiz_statistics.index>`_

      :rtype: :class:`canvasAPI.paginated_list.PaginatedList`
      """
      return PaginatedList(
         self._requester,
         "GET",
         "courses/{}/quizzes/{}/statistics".format(course_id, quiz_id),
         {"course_id": course_id},
         _root="quiz_statistics",
         _kwargs=combine_kwargs(**kwargs),
      )

   def get_submissions(self, course_id, quiz_id, **kwargs):
      """
      Get a list of all submissions for this quiz.

      :calls: `GET /api/v1/courses/:course_id/quizzes/:quiz_id/submissions \
      <https://canvas.instructure.com/doc/api/quiz_submissions.html#method.quizzes/quiz_submissions_api.index>`_

      :rtype: :class:`canvasAPI.paginated_list.PaginatedList`
      """
      return PaginatedList(
         self._requester,
         "GET",
         "courses/{}/quizzes/{}/submissions".format(course_id, quiz_id),
         {"course_id": course_id},
         _root="quiz_submissions",
         _kwargs=combine_kwargs(**kwargs),
      )

   def set_extensions(self, course_id, quiz_id, quiz_extensions, **kwargs):
      """
      Set extensions for student quiz submissions.

      :calls: `POST /api/v1/courses/:course_id/quizzes/:quiz_id/extensions
         <https://canvas.instructure.com/doc/api/quiz_extensions.html#method.quizzes/quiz_extensions.create>`_

      :param quiz_extensions: List of dictionaries representing extensions.
      :type quiz_extensions: list

      :rtype: list of quiz extension dictionaires

      Example Usage:

      >>> quiz.set_extensions([
      ...     {
      ...         'user_id': 1,
      ...         'extra_time': 60,
      ...         'extra_attempts': 1
      ...     },
      ...     {
      ...         'user_id': 2,
      ...         'extra_attempts': 3
      ...     },
      ...     {
      ...         'user_id': 3,
      ...         'extra_time': 20
      ...     }
      ... ])
      """

      if not isinstance(quiz_extensions, list) or not quiz_extensions:
         raise ValueError("Param `quiz_extensions` must be a non-empty list.")

      if any(not isinstance(extension, dict) for extension in quiz_extensions):
         raise ValueError("Param `quiz_extensions` must only contain dictionaries")

      if any("user_id" not in extension for extension in quiz_extensions):
         raise RequiredFieldMissing(
               "Dictionaries in `quiz_extensions` must contain key `user_id`"
         )

      kwargs["quiz_extensions"] = quiz_extensions

      response = self._requester.request(
         "POST",
         "courses/{}/quizzes/{}/extensions".format(course_id, quiz_id),
         _kwargs=combine_kwargs(**kwargs),
      )
      extension_list = response.json()["quiz_extensions"]
      return extension_list


class QuizSubmission(CanvasObject):
      
   def complete(self, course_id, quiz_id, quiz_submission_id, attempt, validation_token=None, **kwargs):
      """
      Complete the quiz submission by marking it as complete and grading it. When the quiz
      submission has been marked as complete, no further modifications will be allowed.


      :calls: `POST /api/v1/courses/:course_id/quizzes/:quiz_id/submissions/:id/complete \
      <https://canvas.instructure.com/doc/api/quiz_submissions.html#method.quizzes/quiz_submissions_api.complete>`_

      :param validation_token: (Optional) The unique validation token for this quiz submission.
      :type validation_token: str
      :rtype: dict
      """
      try:
         kwargs["validation_token"] = validation_token
      except AttributeError:
         raise RequiredFieldMissing(
               "`validation_token` not set on this QuizSubmission, must be passed"
               " as a function argument."
         )

      # Only the latest attempt for a quiz submission can be updated, and Canvas
      # automatically returns the latest attempt with every quiz submission response,
      # so we can just use that.
      kwargs["attempt"] = attempt

      response = self._requester.request(
         "POST",
         "courses/{}/quizzes/{}/submissions/{}/complete".format(
               course_id, quiz_id, quiz_submission_id
         ),
         _kwargs=combine_kwargs(**kwargs),
      )

      response_json = response.json()["quiz_submissions"][0]
      return response_json

   def get_submission_events(self, course_id, quiz_id, quiz_submission_id, **kwargs):
      """
      Retrieve the set of events captured during a specific submission attempt.

      :calls: `GET /api/v1/courses/:course_id/quizzes/:quiz_id/submissions/:id/events \
      <https://canvas.instructure.com/doc/api/quiz_submission_events.html#method.quizzes/quiz_submission_events_api.index>`_

      :rtype: :class:`canvasAPI.paginated_list.PaginatedList`
      """
      return PaginatedList(
         self._requester,
         "GET",
         "courses/{}/quizzes/{}/submissions/{}/events".format(
               course_id, quiz_id, quiz_submission_id
         ),
         _root="quiz_submission_events",
         _kwargs=combine_kwargs(**kwargs),
      )

   def get_submission_questions(self, quiz_submission_id, attempt, **kwargs):
      """
      Get a list of all the question records for this quiz submission.

      :calls: `GET /api/v1/quiz_submissions/:quiz_submission_id/questions \
      <https://canvas.instructure.com/doc/api/quiz_submission_questions.html#method.quizzes/quiz_submission_questions.index>`_

      :returns: A list of quiz submission questions.
      :rtype: list of dictionaries
      """
      response = self._requester.request(
         "GET",
         "quiz_submissions/{}/questions".format(quiz_submission_id),
         _kwargs=combine_kwargs(**kwargs),
      )

      questions = list()
      for question in response.json().get("quiz_submission_questions", []):
         question.update({"quiz_submission_id": quiz_submission_id, "attempt": attempt})
         questions.append(question)

      return questions

   def get_times(self, course_id, quiz_id, quiz_submission_id, **kwargs):
      """
      Get the current timing data for the quiz attempt, both the end_at timestamp and the
      time_left parameter.

      :calls: `GET /api/v1/courses/:course_id/quizzes/:quiz_id/submissions/:id/time \
      <https://canvas.instructure.com/doc/api/quiz_submissions.html#method.quizzes/quiz_submissions_api.time>`_

      :rtype: dict
      """
      response = self._requester.request(
         "GET",
         "courses/{}/quizzes/{}/submissions/{}/time".format(
               course_id, quiz_id, quiz_submission_id
         ),
         _kwargs=combine_kwargs(**kwargs),
      )

      return response.json()

   def update_score_and_comments(self, course_id, quiz_id, quiz_submission_id, **kwargs):
      """
      Update the amount of points a student has scored for questions they've answered, provide
      comments for the student about their answer(s), or simply fudge the total score by a
      specific amount of points.

      :calls: `PUT /api/v1/courses/:course_id/quizzes/:quiz_id/submissions/:id \
      <https://canvas.instructure.com/doc/api/quiz_submissions.html#method.quizzes/quiz_submissions_api.update>`_

      :returns: The updated quiz.
      :rtype: dict
      """
      response = self._requester.request(
         "PUT",
         "courses/{}/quizzes/{}/submissions/{}".format(
               course_id, quiz_id, quiz_submission_id
         ),
         _kwargs=combine_kwargs(**kwargs),
      )
      response_json = response.json()["quiz_submissions"][0]
      response_json.update({"course_id": course_id})

      return response_json


class QuizQuestion(CanvasObject):

   def delete(self, course_id, quiz_id, quiz_question_id, **kwargs):
      """
      Delete an existing quiz question.

      :calls: `DELETE /api/v1/courses/:course_id/quizzes/:quiz_id/questions/:id \
      <https://canvas.instructure.com/doc/api/quiz_questions.html#method.quizzes/quiz_questions.destroy>`_

      :returns: True if question was successfully deleted; False otherwise.
      :rtype: bool
      """
      response = self._requester.request(
         "DELETE",
         "courses/{}/quizzes/{}/questions/{}".format(
               course_id, quiz_id, quiz_question_id
         ),
         _kwargs=combine_kwargs(**kwargs),
      )

      return response.status_code == 204

   def edit(self, course_id, quiz_id, quiz_question_id, **kwargs):
      """
      Update an existing quiz question.

      :calls: `PUT /api/v1/courses/:course_id/quizzes/:quiz_id/questions/:id \
      <https://canvas.instructure.com/doc/api/quiz_questions.html#method.quizzes/quiz_questions.update>`_

      :rtype: dict
      """
      response = self._requester.request(
         "PUT",
         "courses/{}/quizzes/{}/questions/{}".format(
               course_id, quiz_id, quiz_question_id 
         ),
         _kwargs=combine_kwargs(**kwargs),
      )
      response_json = response.json()
      response_json.update({"course_id": course_id})

      return response_json


class QuizReport(CanvasObject):

   def abort_or_delete(self, course_id, quiz_id, quiz_report_id, **kwargs):
      """
      This API allows you to cancel a previous request you issued for a report to be generated.
      Or in the case of an already generated report, you'd like to remove it, perhaps to generate
      it another time with an updated version that provides new features.

      :calls: `DELETE /api/v1/courses/:course_id/quizzes/:quiz_id/reports/:id \
      <https://canvas.instructure.com/doc/api/quiz_reports.html#method.quizzes/quiz_reports.abort>`_

      :returns: True if attempt was successful; False otherwise
      :rtype: bool
      """
      response = self._requester.request(
         "DELETE",
         "courses/{}/quizzes/{}/reports/{}".format(
               course_id, quiz_id, quiz_report_id
         ),
         _kwargs=combine_kwargs(**kwargs),
      )

      return response.status_code == 204

