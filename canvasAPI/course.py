from logging import exception

from requests.api import request
from .canvas_object import CanvasObject
from .paginated_list import PaginatedList
from .exceptions import RequiredFieldMissing
from .upload import Uploader, FileOrPathLike
from .util import combine_kwargs
import requests
from canvasapi import Canvas
import os
import xml.etree.ElementTree as ET


def generate_qti_xml(questions):
    root = ET.Element(
        "assessment",
        {
            "xmlns": "http://www.imsglobal.org/xsd/imsqti_v2p1",
            "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
            "xsi:schemaLocation": "http://www.imsglobal.org/xsd/imsqti_v2p1 ims_qti_v2p1.xsd",
        },
    )
    for index, question in enumerate(questions):
        item = ET.SubElement(root, "item", {"ident": f"item_{index+1}"})
        itemmetadata = ET.SubElement(item, "itemmetadata")
        title = ET.SubElement(itemmetadata, "title")
        title.text = question.question_name
        presentation = ET.SubElement(item, "presentation")
        response_str = ""
        for index, answer in enumerate(question.answers):
            response_str += f'{chr(65 + index)}. {answer["text"]}\n'
        material = ET.SubElement(presentation, "material")
        materialtext = ET.SubElement(material, "materialtext")
        materialtext.text = response_str

    return ET.tostring(root, encoding="utf-8", method="xml")

    def canvas_api_get(endpoint, params=None):
        API_URL = "https://your_canvas_instance/api/v1"
        ACCESS_TOKEN = os.getenv("CANVAS_ACCESS_TOKEN")
        headers = {"Authorization": "Bearer " + ACCESS_TOKEN}
        response = requests.get(API_URL + endpoint, headers=headers, params=params)
        response.raise_for_status()
        return response.json()


class Course(CanvasObject):
    # def get_course(self, course_id, **kwargs):
    #    """
    #    Retrieve a course by its ID.
    #    :calls: `GET /api/v1/courses/:id \
    #    <https://canvas.instructure.com/doc/api/courses.html#method.courses.show>`_
    #    :param course_id: The ID of the course to retrieve.
    #    :type course: int
    #    :rtype: dict
    #    """
    #    uri_str = "courses/{}"

    #    response = self._requester.request(
    #       "GET",
    #       uri_str.format(course_id),
    #       _kwargs=combine_kwargs(**kwargs)
    #    )
    #    return response.json()

    def get_favorites(self, **kwargs):
        """
        Retrieve a list of favorited courses for the current user
        :calls: GET users/self/favorites/courses
        'https://canvas.instructure.com/doc/api/favorites.html'
        """
        uri = "users/self/favorites/courses"

        return PaginatedList(
            self._requester, "GET", uri, _kwargs=combine_kwargs(**kwargs)
        )

    def create_folder(self, course_id, name, **kwargs):
        """
        Creates a folder in this course.
        :calls: `POST /api/v1/courses/:course_id/folders
        <https://canvas.instructure.com/doc/api/files.html#method.folders.create>`_
        :param name: The name of the folder.
        """
        response = self._requester.request(
            "POST",
            "courses/{}/folders".format(course_id),
            name=name,
            _kwargs=combine_kwargs(**kwargs),
        )
        return response.json()

    def create_group_category(self, course_id, name, **kwargs):
        """
      Create a group category.
      :calls: `POST /api/v1/courses/:course_id/group_categories \
      <https://canvas.instructure.com/doc/api/group_categories.html#method.group_categories.create>`_
      :param name: Name of the category.
      :type name: str
      :rtype: dict
      """

        response = self._requester.request(
            "POST",
            "courses/{}/group_categories".format(course_id),
            name=name,
            _kwargs=combine_kwargs(**kwargs),
        )
        return response.json()

    def create_module(self, course_id, module, **kwargs):
        """
      Create a new module.
      :calls: `POST /api/v1/courses/:course_id/modules \
      <https://canvas.instructure.com/doc/api/modules.html#method.context_modules_api.create>`_
      :param module: The attributes for the module.
      :type module: dict
      :returns: The created module.
      :rtype: dict
      """
        if isinstance(module, dict) and "name" in module:
            kwargs["module"] = module
        else:
            raise RequiredFieldMissing("Dictionary with key 'name' is required.")

        response = self._requester.request(
            "POST",
            "courses/{}/modules".format(course_id),
            _kwargs=combine_kwargs(**kwargs),
        )
        module_json = response.json()
        module_json.update({"course_id": course_id})

        return module_json

    def create_page(self, course_id, wiki_page, **kwargs):
        """
      Create a new wiki page.
      :calls: `POST /api/v1/courses/:course_id/pages \
      <https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.create>`_
      :param wiki_page: The title for the page.
      :type wiki_page: dict
      :returns: The created page.
      :rtype: dict
      """

        if isinstance(wiki_page, dict) and "title" in wiki_page:
            kwargs["wiki_page"] = wiki_page
        else:
            raise RequiredFieldMissing("Dictionary with key 'title' is required.")

        response = self._requester.request(
            "POST",
            "courses/{}/pages".format(course_id),
            _kwargs=combine_kwargs(**kwargs),
            json=False,
        )

        page_json = response.json()
        page_json.update({"course_id": course_id})

        return page_json

    def create_quiz(self, course_id, quiz, **kwargs):
        """
      Create a new quiz in this course.
      :calls: `POST /api/v1/courses/:course_id/quizzes \
      <https://canvas.instructure.com/doc/api/quizzes.html#method.quizzes/quizzes_api.create>`_
      :param quiz: The attributes for the quiz.
      :type quiz: dict
      :rtype: dict
      """

        if isinstance(quiz, dict) and "title" in quiz:
            kwargs["quiz"] = quiz
        else:
            raise RequiredFieldMissing("Dictionary with key 'title' is required.")

        response = self._requester.request(
            "POST",
            "courses/{}/quizzes".format(course_id),
            _kwargs=combine_kwargs(**kwargs),
        )
        quiz_json = response.json()
        quiz_json.update({"course_id": course_id})

        return quiz_json

    def create_rubric(self, course_id, **kwargs):
        """
      Create a new rubric.
      :calls: `POST /api/v1/courses/:course_id/rubrics \
      <https://canvas.instructure.com/doc/api/rubrics.html#method.rubrics.create>`_
      :rtype: `dict`
      """
        response = self._requester.request(
            "POST",
            "courses/{}/rubrics".format(course_id),
            _kwargs=combine_kwargs(**kwargs),
        )

        return response.json()

    def get_assignment(self, course_id, assignment_id, **kwargs):
        """
      Return the assignment with the given ID from the given course.
      :calls: `GET /api/v1/courses/:course_id/assignments/:id \
      <https://canvas.instructure.com/doc/api/assignments.html#method.assignments_api.show>`_
      :param assignment_id: The object or ID of the assignment to retrieve.
      :type assignment: int
      """

        response = self._requester.request(
            "GET",
            "courses/{}/assignments/{}".format(course_id, assignment_id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return response.json()

    def get_assignments(self, course_id, **kwargs):
        """
      List all of the assignments in this course.
      :calls: `GET /api/v1/courses/:course_id/assignments \
      <https://canvas.instructure.com/doc/api/assignments.html#method.assignments_api.index>`_
      :rtype: :class:`canvasAPI.paginated_list.PaginatedList` of
         :class:`canvasAPI.assignment.Assignment`
      """
        response = self._requester.request(
            "GET",
            "courses/{}/assignments".format(course_id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return response

    def get_assignments_for_group(self, course_id, assignment_group_id, **kwargs):
        """
      Returns a paginated list of assignments for the given assignment group
      :calls: `GET /api/v1/courses/:course_id/assignment_groups/:assignment_group_id/assignments\
      <https://canvas.instructure.com/doc/api/assignments.html#method.assignments_api.index>`_

      :rtype: :class:`canvasAPI.paginated_list.PaginatedList`
      """
        return PaginatedList(
            self._requester,
            "GET",
            "courses/{}/assignment_groups/{}/assignments".format(
                course_id, assignment_group_id
            ),
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_collaborations(self, course_id, **kwargs):
        """
      Return a list of collaborations for a given course ID.
      :calls: `GET /api/v1/courses/:course_id/collaborations \
      <https://canvas.instructure.com/doc/api/collaborations.html#method.collaborations.api_index>`_
      :rtype: :class:`canvasAPI.paginated_list.PaginatedList`
      """
        return PaginatedList(
            self._requester,
            "GET",
            "courses/{}/collaborations".format(course_id),
            _root="collaborations",
            kwargs=combine_kwargs(**kwargs),
        )

    def get_potential_collaborators(self, course_id, **kwargs):
        """
        Returns a paginated list of the users who can potentially be added to a
        collaboration in the course.

        :calls: `GET /api/v1/courses/:course_id/potential_collaborators
        <https://canvas.instructure.com/doc/api/collaborations.html#method.collaborations.potential_collaborators>`_
        :rtype: :class:`canvasAPI.paginated_list.PaginatedList`
        """
        return PaginatedList(
            self._requester,
            "GET",
            "courses/{}/potential_collaborators".format(course_id),
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_enrollments(self, course_id, **kwargs):
        """
      List all of the enrollments in this course.
      :calls: `GET /api/v1/courses/:course_id/enrollments \
      <https://canvas.instructure.com/doc/api/enrollments.html#method.enrollments_api.index>`_
      :rtype: :class:`canvasapi.paginated_list.PaginatedList`
      """
        return PaginatedList(
            self._requester,
            "GET",
            "courses/{}/enrollments".format(course_id),
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_files(self, course_id, **kwargs):
        """
      Returns the paginated list of all files for the given course.
      :calls: `GET /api/v1/courses/:course_id/files \
      <https://canvas.instructure.com/doc/api/files.html#method.files.api_index>`_
      :rtype: :class:`canvasAPI.paginated_list.PaginatedList`
      """
        return PaginatedList(
            self._requester,
            "GET",
            "courses/{}/files".format(course_id),
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_folder(self, course_id, folder_id, **kwargs):
        """
      Returns the details for a course folder
      :calls: `GET /api/v1/courses/:course_id/folders/:id \
      <https://canvas.instructure.com/doc/api/files.html#method.folders.show>`_
      :rtype: dict
      """
        response = self._requester.request(
            "GET",
            "courses/{}/folders/{}".format(course_id, folder_id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return response.json()

    def get_folders(self, course_id, **kwargs):
        """
      Returns the paginated list of all folders for the given course. This will be returned as a
      flat list containing all subfolders as well.
      :calls: `GET /api/v1/courses/:course_id/folders \
      <https://canvas.instructure.com/doc/api/files.html#method.folders.list_all_folders>`_
      :rtype: :class:`canvasAPI.paginated_list.PaginatedList`
      """
        return PaginatedList(
            self._requester,
            "GET",
            "courses/{}/folders".format(course_id),
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_groups(self, course_id, **kwargs):
        """
      Return list of active groups for the specified course.
      :calls: `GET /api/v1/courses/:course_id/groups \
      <https://canvas.instructure.com/doc/api/groups.html#method.groups.context_index>`_
      :rtype: :class:`canvasAPI.paginated_list.PaginatedList`
      """
        return PaginatedList(
            self._requester,
            "GET",
            "courses/{}/groups".format(course_id),
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_group_categories(self, course_id, **kwargs):
        """
      List group categories for a context.
      :calls: `GET /api/v1/courses/:course_id/group_categories \
      <https://canvas.instructure.com/doc/api/group_categories.html#method.group_categories.index>`_
      :rtype: :class:`canvasAPI.paginated_list.PaginatedList`
      """

        return PaginatedList(
            self._requester,
            "GET",
            "courses/{}/group_categories".format(course_id),
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_module(self, course_id, module_id, **kwargs):
        """
      Retrieve a single module by ID.
      :calls: `GET /api/v1/courses/:course_id/modules/:id \
      <https://canvas.instructure.com/doc/api/modules.html#method.context_modules_api.show>`_
      :rtype: dict
      """

        response = self._requester.request(
            "GET",
            "courses/{}/modules/{}".format(course_id, module_id),
            _kwargs=combine_kwargs(**kwargs),
        )

        module_json = response.json()
        module_json.update({"course_id": course_id})

        return module_json

    def get_modules(self, course_id, **kwargs):
        """
      Return a list of modules in this course.
      :calls: `GET /api/v1/courses/:course_id/modules \
      <https://canvas.instructure.com/doc/api/modules.html#method.context_modules_api.index>`_
      :rtype: :class:`canvasapi.paginated_list.PaginatedList`
      """
        return PaginatedList(
            self._requester,
            "GET",
            "courses/{}/modules".format(course_id),
            {"course_id": course_id},
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_multiple_submissions(self, course_id, **kwargs):
        """
      List submissions for multiple assignments.
      Get all existing submissions for a given set of students and assignments.
      :calls: `GET /api/v1/courses/:course_id/students/submissions \
      <https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.for_students>`_
      :rtype: :class:`canvasapi.paginated_list.PaginatedList`
      """
        return PaginatedList(
            self._requester,
            "GET",
            "courses/{}/students/submissions".format(course_id),
            {"course_id": course_id},
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_quiz(self, course_id, quiz_id, **kwargs):
        """
      Return the quiz with the given id.
      :calls: `GET /api/v1/courses/:course_id/quizzes/:id \
      <https://canvas.instructure.com/doc/api/quizzes.html#method.quizzes/quizzes_api.show>`_
      :rtype: dict
      """
        print(os.getenv("CANVAS_ACCESS_TOKEN"))
        response = self._requester.request(
            "GET",
            "courses/{}/quizzes/{}".format(course_id, quiz_id),
            _kwargs=combine_kwargs(**kwargs),
        )
        quiz_json = response.json()
        quiz_json.update({"course_id": course_id})

        return quiz_json

    def get_quiz_overrides(self, course_id, **kwargs):
        """
      Retrieve the actual due-at, unlock-at,
      and available-at dates for quizzes based on
      the assignment overrides active for the current API user.
      :calls: `GET /api/v1/courses/:course_id/quizzes/assignment_overrides \
      <https://canvas.instructure.com/doc/api/quiz_assignment_overrides.html#method.quizzes/quiz_assignment_overrides.index>`_
      :rtype: :class:`canvasAPI.paginated_list.PaginatedList`
      """

        return PaginatedList(
            self._requester,
            "GET",
            "courses/{}/quizzes/assignment_overrides".format(course_id),
            _root="quiz_assignment_overrides",
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_quizzes(self, course_id, **kwargs):
        """
      Return a list of quizzes belonging to this course.
      :calls: `GET /api/v1/courses/:course_id/quizzes \
      <https://canvas.instructure.com/doc/api/quizzes.html#method.quizzes/quizzes_api.index>`_
      :rtype: :class:`canvasAPI.paginated_list.PaginatedList`
      """

        return PaginatedList(
            self._requester,
            "GET",
            "courses/{}/quizzes".format(course_id),
            {"course_id": course_id},
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_page(self, course_id, page_url_or_id, **kwargs):
        """
      Retrieve the contents of a wiki page.
      :calls: `GET /api/v1/courses/:course_id/pages/:url_or_id \
      <https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.show>`_
      :param url_or_id: The url or id for the page.
      :type url: str
      :type id: int
      :returns: The specified page.
      :rtype: dict
      """

        response = self._requester.request(
            "GET",
            "courses/{}/pages/{}".format(course_id, page_url_or_id),
            _kwargs=combine_kwargs(**kwargs),
        )
        page_json = response.json()
        page_json.update({"course_id": course_id})

        return page_json

    def get_pages(self, course_id, **kwargs):
        """
      List the wiki pages associated with a course.
      :calls: `GET /api/v1/courses/:course_id/pages \
      <https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.index>`_
      :rtype: :class:`canvasAPI.paginated_list.PaginatedList`
      """
        return PaginatedList(
            self._requester,
            "GET",
            "courses/{}/pages".format(course_id),
            {"course_id": course_id},
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_rubric(self, course_id, rubric_id, **kwargs):
        """
      Get a single rubric, based on rubric id.
      :calls: `GET /api/v1/courses/:course_id/rubrics/:id \
      <https://canvas.instructure.com/doc/api/rubrics.html#method.rubrics_api.show>`_
      :param rubric_id: The ID of the rubric.
      :type rubric_id: int
      :rtype: dict
      """
        response = self._requester.request(
            "GET",
            "courses/%s/rubrics/%s" % (course_id, rubric_id),
            _kwargs=combine_kwargs(**kwargs),
        )

        response_json = response.json()
        response_json.update({"course_id": course_id})

        return response_json

    def get_rubrics(self, course_id, **kwargs):
        """
      Get the paginated list of active rubrics for the current course.
      :calls: `GET /api/v1/courses/:course_id/rubrics \
      <https://canvas.instructure.com/doc/api/rubrics.html#method.rubrics_api.index>`_
      :rtype: :class:`canvasapi.paginated_list.PaginatedList`
      """
        return PaginatedList(
            self._requester,
            "GET",
            "courses/%s/rubrics" % (course_id),
            {"course_id": course_id},
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_section(self, course_id, section_id, **kwargs):
        """
      Retrieve a section.
      :calls: `GET /api/v1/courses/:course_id/sections/:id \
      <https://canvas.instructure.com/doc/api/sections.html#method.sections.show>`_
      :rtype: dict
      """

        response = self._requester.request(
            "GET",
            "courses/{}/sections/{}".format(course_id, section_id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return response.json()

    def get_sections(self, course_id, **kwargs):
        """
      List all sections in a course.
      :calls: `GET /api/v1/courses/:course_id/sections \
      <https://canvas.instructure.com/doc/api/sections.html#method.sections.index>`_
      :rtype: :class:`canvasapi.paginated_list.PaginatedList`
      """

        return PaginatedList(
            self._requester,
            "GET",
            "courses/{}/sections".format(course_id),
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_user(self, course_id, user_id, **kwargs):
        """
      Retrieve a user by their ID.
      :calls: `GET /api/v1/courses/:course_id/users/:id \
      <https://canvas.instructure.com/doc/api/courses.html#method.courses.user>`_
      :rtype: dict
      """

        uri = "courses/{}/users/{}".format(course_id, user_id)

        response = self._requester.request("GET", uri, _kwargs=combine_kwargs(**kwargs))
        return response.json()

    def get_users(self, course_id, **kwargs):
        """
      List all users in a course.
      :calls: `GET /api/v1/courses/:course_id/search_users \
      <https://canvas.instructure.com/doc/api/courses.html#method.courses.users>`_
      :rtype: :class:`canvasAPI.paginated_list.PaginatedList`
      """

        return PaginatedList(
            self._requester,
            "GET",
            "courses/{}/search_users".format(course_id),
            _kwargs=combine_kwargs(**kwargs),
        )

    def get_settings(self, course_id, **kwargs):
        """
      Returns this course's settings.
      :calls: `GET /api/v1/courses/:course_id/settings \
      <https://canvas.instructure.com/doc/api/courses.html#method.courses.settings>`_
      :rtype: dict
      """
        response = self._requester.request(
            "GET",
            "courses/{}/settings".format(course_id),
            _kwargs=combine_kwargs(**kwargs),
        )
        return response.json()

    def update_settings(self, course_id, **kwargs):
        """
      Update a course's settings.
      :calls: `PUT /api/v1/courses/:course_id/settings \
      <https://canvas.instructure.com/doc/api/courses.html#method.courses.update_settings>`_
      :rtype: dict
      """
        response = self._requester.request(
            "PUT", "courses/{}/settings".format(course_id), **kwargs
        )
        return response.json()

    def get_tabs(self, course_id, **kwargs):
        """
      List available tabs for a course.
      Returns a list of navigation tabs available in the current context.
      :calls: `GET /api/v1/courses/:course_id/tabs \
      <https://canvas.instructure.com/doc/api/tabs.html#method.tabs.index>`_
      :rtype: :class:`canvasapi.paginated_list.PaginatedList`
      """
        return PaginatedList(
            self._requester,
            "GET",
            "courses/{}/tabs".format(course_id),
            {"course_id": course_id},
            _kwargs=combine_kwargs(**kwargs),
        )

    def update(self, course_id, **kwargs):
        """
      Update this course.
      :calls: `PUT /api/v1/courses/:id \
      <https://canvas.instructure.com/doc/api/courses.html#method.courses.update>`_
      :returns: `True` if the course was updated, `False` otherwise.
      :rtype: `bool`
      """
        response = self._requester.request(
            "PUT", "courses/{}".format(course_id), _kwargs=combine_kwargs(**kwargs)
        )

        return response.json().get("name")

    def update_tab(self, course_id, tab_id, **kwargs):
        """
      Update a tab for a course.

      Note: Home and Settings tabs are not manageable, and can't be
      hidden or moved.

      :calls: `PUT /api/v1/courses/:course_id/tabs/:tab_id \
      <https://canvas.instructure.com/doc/api/tabs.html#method.tabs.update>`_
      :rtype: dict
      """

        response = self._requester.request(
            "PUT",
            "courses/{}/tabs/{}".format(course_id, tab_id),
            _kwargs=combine_kwargs(**kwargs),
        )
        response_json = response.json()
        response_json.update({"course_id": course_id})

        return response_json

    def upload(self, course_id, file: FileOrPathLike, **kwargs):
        """
      Upload a file to this course.
      :calls: `POST /api/v1/courses/:course_id/files \
      <https://canvas.instructure.com/doc/api/courses.html#method.courses.create_file>`_
      :param file: The file or path of the file to upload.
      :type file: file or str
      :returns: True if the file uploaded successfully, False otherwise, \
                  and the JSON response from the API.
      :rtype: tuple
      """
        return Uploader(
            self._requester, "courses/{}/files".format(course_id), file, **kwargs
        ).start()

    # ------------------------------------------------------------------------------
    ### Author: by Pooja Pal
    # ------------------------------------------------------------------------------
    def get_course(self, courseId, **kwargs):
        """
        Retrieve a course by its ID.
        :param courseId: The ID of the course that to be retrieved.
        :type course: string
        :rtype: Http Response object
        """
        uri_str = "courses/{}"
        kwargs["per_page"] = 50
        kwargs["include"] = ["syllabus_body", "term"]
        response = self._requester.request(
            "GET", uri_str.format(courseId), _kwargs=combine_kwargs(**kwargs)
        )
        return response

    def get_courses(self, **kwargs):
        """
        fetches list of enrolled courses for the current user.
        :param courseId: The ID of the course that to be retrieved.
        :type course: string
        :rtype: Http Response object
        """
        kwargs["per_page"] = 50
        kwargs["include"] = ["syllabus_body", "term"]
        endpoint = "users/self/courses"
        response = self._requester.request(
            "GET", endpoint, _kwargs=combine_kwargs(**kwargs)
        )
        return response

    def getCourseStudents(self, courseId, **kwargs):
        """
        Fetches a list students in a course
        :param courseId: The ID of the course that to be retrieved.
        :type course: string
        :rtype: Http Response object
        """
        kwargs["per_page"] = "50"
        response = self._requester.request(
            "GET",
            "courses/{}/students".format(courseId),
            _kwargs=combine_kwargs(**kwargs),
        )
        return response

    # ------------------------------------AUTHOR : Karan Chopra

    def import_qti_quiz(self, courseId, quizName, **kwargs):
        payload = {
            "quiz": {
                "title": "{}".format(quizName),  # Replace with your quiz title
            }
        }

        headers = {
            "Authorization": "Bearer 10~dVERK37nMXapiXX17crpLcI5jJhufVIAnEw2MacMgxR8nnuGwo8xaGVz3Lm8VSRW"
        }

        result = requests.post(
            "https://canvas.uw.edu/api/v1/courses/{}/quizzes".format(courseId),
            json=payload,
            headers=headers,
        )
        ans = result.json()
        return {"ans": ans}

    def export_All_Qti(self, courseId):
        return {"in canvas api function"}

    def export_qti_quiz(self, courseId, quizId):
        headers = {
            "Authorization": "Bearer 10~dVERK37nMXapiXX17crpLcI5jJhufVIAnEw2MacMgxR8nnuGwo8xaGVz3Lm8VSRW"
        }

        result = requests.get(
            "https://canvas.uw.edu/api/v1/courses/{}/quizzes/{}/questions".format(
                courseId, quizId
            ),
            headers=headers,
        )
        quesArr = result.json()

        path = "quiz.txt"
        with open(path, "w") as file:
            for question in quesArr:
                file.write(question["question_name"] + "\n")
                file.write(question["question_text"] + "\n")
                for ans in question["answers"]:
                    file.write(ans["text"] + " - " + str(ans["weight"]) + "\n")
                file.write("\n")

        return {"result": quesArr}
