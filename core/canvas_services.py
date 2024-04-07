import json
import os, csv, wget
from flask import jsonify

# Canvas Functions
import canvasFunctions.assignments
import canvasFunctions.courses
import canvasFunctions.quizzes
import canvasFunctions.settings
import canvasFunctions.students
import canvasFunctions.pages
from canvasFunctions.util import getDictSubset, getSubset

# Models
from models.assignment import Assignment
from models.course import Course
from models.folder import Folder, File
from models.group import Group, GroupCategory
from models.page import Page
from models.quiz import Quiz
from models.user import User

# Canvas API
from canvasAPI.canvas import Canvas
from canvasAPI.util import depaginate

# QTI quiz
import xml.etree.ElementTree as ET


def generate_qti_quiz(text_content):
    # Create the root element for the QTI XML
    root = ET.Element("assessmentItem")
    root.set("xmlns", "http://www.imsglobal.org/xsd/imsqti_v2p1")
    # Create the response declaration for the multiple choice question
    response_declaration = ET.SubElement(
        root,
        "responseDeclaration",
        identifier="RESPONSE",
        cardinality="single",
        baseType="identifier",
    )
    # Create the correct response for the multiple choice question
    correct_response = ET.SubElement(response_declaration, "correctResponse")
    value = ET.SubElement(correct_response, "value")
    value.text = "A"  # Assuming the correct answer is option A
    # Create the item body
    item_body = ET.SubElement(root, "itemBody")
    p = ET.SubElement(item_body, "p")
    p.text = text_content
    # Create the choices for the multiple choice question
    choice_interaction = ET.SubElement(
        root,
        "choiceInteraction",
        responseIdentifier="RESPONSE",
        shuffle="true",
        maxChoices="1",
    )
    # Example choices (you would need to customize this based on your actual choices)
    choices = ["A. Option A", "B. Option B", "C. Option C", "D. Option D"]
    # Add each choice as a simpleChoice element
    for choice_text in choices:
        simple_choice = ET.SubElement(choice_interaction, "simpleChoice")
        simple_choice.text = choice_text
    # Return the XML as a string
    return ET.tostring(root, encoding="unicode")


class canvas_services:
    """
    The main class to be instantiated to perform Canvas operations and to
    provide access to Canvas's API.
    """

    def __init__(self, base_url, canvas_headers):
        """
        :param base_url: The base URL of the Canvas instance's API.
        :type base_url: str
        :param access_token: The API key to authenticate requests with.
        :type access_token: json
        """

        self.canvasapi = Canvas(base_url, canvas_headers)

    # ---COURSES----------------------------------------------------------------

    def getCourseData(self, courseID, **kwargs):
        """return the data for a given course"""
        response = self.canvasapi.course.get_course(courseID, **kwargs)
        return response

    def getCourse(self, courseID, **kwargs):
        """retrieve data from canvas api and return a course model"""
        response = self.canvasapi.course.get_course(courseID, **kwargs)

        return Course(response.json())

    def getCoursesData(self, subset=None, **kwargs):
        """
        Return a list of courses data for the current user.
        If a subset is included in the args, it will return a list of
        course dictionaries with subset key values.
        Example: subset = ('name', 'id')
        Return: [{'name': value, 'id': value}]
        """
        coursePagList = self.canvasapi.course.get_courses(**kwargs)

        courseList = []
        for item in coursePagList:
            if "access_restricted_by_date" in item.json():
                continue
            if item.get("name") is not None:
                if subset:
                    courseList.append(getDictSubset(item, subset))
                else:
                    courseList.append(item)
        return courseList

    def getCourses(self, **kwargs):
        """
        Return a list of active courses as course model objects.
        """
        coursePagList = self.canvasapi.course.get_courses(**kwargs)

        courses = []
        for item in coursePagList:
            if "access_restricted_by_date" in item:
                continue
            if item.get("name") is not None:
                courses.append(Course(item))
        return courses

    def getFavorites(self, subset=None, **kwargs):
        """
        Retrieve a list of favorited courses for the current user.
        If a subset is included in the args, it will return a list of
        course dictionaries with subset key values.
        Example: subset = ('name', 'id')
        Return: [{'name': value, 'id': value, 'role':value}]
        """
        favorites = []
        courses = self.canvasapi.course.get_favorites(include="favorites", per_page=50)
        for course in courses:
            entry = {
                "name": course["name"],
                "id": course["id"],
                "role": course["enrollments"][0]["type"],
            }
            favorites.append(entry)
        return favorites

    # ---STUDENTS---------------------------------------------------------------

    def getStudentsData(self, courseID, **kwargs):
        """returns a list of students data in a course"""
        studentPagList = self.canvasapi.course.get_users(
            courseID, enrollment_type="student", **kwargs
        )
        students = depaginate(studentPagList)
        return students

    def getStudents(self, courseID, **kwargs):
        """returns a list of student User model objects"""
        return self.getUsers(courseID, enrollment_type="student", **kwargs)

    def getUsersData(self, courseID, **kwargs):
        """returns a list of students data in a course"""
        userPagList = self.canvasapi.course.get_users(courseID, **kwargs)
        users = depaginate(userPagList)
        return users

    def getUsers(self, courseID, **kwargs):
        """
        Returns a list of User model objects
        """
        userPagList = self.canvasapi.course.get_users(courseID, **kwargs)
        userList = []
        for item in userPagList:
            user = User(item)
            userList.append(user)
        return userList

    def getUserData(self, userID="self", **kwargs):
        """return the data for a specific user by ID or `self`"""
        user = self.canvasapi.user.get_user(userID, **kwargs)
        return user

    def exportStudents(self, courseID, key="name"):
        """returns a list of the students in a course with a given key"""
        course = self.getCourse(courseID)
        students = self.getStudents(courseID)
        course.addStudents(students)
        return canvasFunctions.students.exportCourseRoster(course, key)

    def exportCourseRoster(self, courseID):
        """Creates a csv file of a course's student names and their ids
        filename: {course name}-Roster.csv
        file rows: student name, student id
        """
        course = self.getCourse(courseID)
        students = self.getStudents(courseID)
        course.addStudents(students)
        return canvasFunctions.students.exportCourseRosterCSV(course)

    # ---GROUPS-----------------------------------------------------------------

    def getGroupsData(self, courseID, **kwargs):
        """returns a list of groups data for a course"""
        groupPagList = self.canvasapi.course.get_groups(courseID, **kwargs)
        groups = depaginate(groupPagList)
        return groups

    def getGroups(self, courseID, **kwargs):
        """returns a list of group model objects"""
        groupPagList = self.canvasapi.course.get_groups(courseID, **kwargs)
        itemList = []
        for item in groupPagList:
            item = Group(item)
            itemList.append(item)
        return itemList

    def getGroupsCategories(self, courseID, **kwargs):
        """
        returns a list of GroupCategory models with a dictionary
        of Group models
        """
        categoryPagList = self.canvasapi.course.get_group_categories(courseID, **kwargs)
        catList = []
        for cat in categoryPagList:
            category = GroupCategory(cat)
            catList.append(category)
            groupPagList = self.canvasapi.group.get_groups_in_category(category.id)
            for group in groupPagList:
                group = Group(group)
                group.setCategoryName(cat)
                category.addGroup(group)
        return catList

    def getGroupsList(self, courseID):
        """returns a list of group dictionaries with the keys: 'name', 'id'"""
        groups = self.getGroupsData(courseID)
        groupsList = []
        for group in groups:
            entry = {"name": group.get("name"), "id": group.get("id")}
            groupsList.append(entry)
        return groupsList

    def exportGroupsJSON(self, courseID, key="name"):
        """exports a JSON of all groups and their members with a given key"""
        course = self.getGroupMembers(courseID)
        if key == "":
            key = "name"
        subset = ("id", key)
        groupsJson = {}
        for group in course.getGroups():
            members = [member.getDictSubset(subset) for member in group.getMembers()]
            groupsJson[group.name] = members
        return groupsJson

    def exportGroupsCSV(self, courseID):
        """Creates a csv file of students and their groups
        from a specified course
        """
        course = self.getGroupMembers(courseID, getGroupCategory=True)
        return canvasFunctions.students.exportGroupCSVModels(course)

    def getGroupMembers(self, courseID, getGroupCategory=False):
        """Gets all students and their groups from a specified course and
        saves the data to a course model
        """
        course = self.getCourse(courseID)
        students = self.getStudents(courseID)
        course.addStudents(students)
        groupPagList = self.canvasapi.course.get_groups(courseID)
        for item in groupPagList:
            group = Group(item)
            course.addGroup(group)
            if getGroupCategory:
                groupCategoryId = group.get("group_category_id")
                if groupCategoryId:
                    category = self.canvasapi.group.get_group_category(groupCategoryId)
                    group.setCategoryName(category)
            memberPagList = self.canvasapi.group.get_users(group.get("id"))
            for user in memberPagList:
                memberID = user.get("id")
                member = course.getStudentById(memberID)
                group.addMember(member)
        return course

    def importStudentGroups(self, courseID, file):
        course = self.getCourse(courseID)
        groupCategories = self.getGroupsCategories(courseID)
        for category in groupCategories:
            course.addGroupCategory(category)

        response = canvasFunctions.students.importGroups(course, file, self.canvasapi)
        return response

    # ---FILE SYSTEM------------------------------------------------------------

    def getFoldersData(self, courseID, **kwargs):
        """returns a list of folders data"""
        response = self.canvasapi.course.get_folders(courseID, **kwargs)
        folders = depaginate(response)
        return folders

    def getFolders(self, courseID, **kwargs):
        """returns a list of folder model objects"""
        response = self.canvasapi.course.get_folders(courseID, **kwargs)
        itemList = []
        for item in response:
            item = Folder(item)
            itemList.append(item)
        return itemList

    def getFoldersList(self, courseID, **kwargs):
        """returns a list of folder names and ids for a given course"""
        folders = self.getFoldersData(courseID, **kwargs)
        foldersList = []
        for folder in folders:
            entry = {"name": folder.get("full_name"), "id": folder.get("id")}
            foldersList.append(entry)
        return foldersList

    def getFilesData(self, courseID, **kwargs):
        """returns a list of files data for a course"""
        response = self.canvasapi.course.get_files(courseID, **kwargs)
        files = depaginate(response)
        return files

    def getFiles(self, courseID, **kwargs):
        """returns a list of file model objects"""
        response = self.canvasapi.course.get_files(courseID, **kwargs)
        itemList = []
        for item in response:
            item = File(item)
            itemList.append(item)
        return itemList

    def deleteFile(self, fileID, **kwargs):
        """delete a Canvas file"""
        response = self.canvasapi.file.delete(fileID, **kwargs)
        return response

    def deleteFolder(self, folderID, **kwargs):
        """delete a Canvas folder"""
        response = self.canvasapi.folder.delete(folderID, **kwargs)
        return response

    def uploadFile(self, courseID, file, **kwargs):
        """upload a file to a course
        To upload to a specific folder, pass: parent_folder_path=folder
        """
        response = self.canvasapi.course.upload(courseID, file, **kwargs)
        return response

    def createCourseFolder(self, courseID, folderName, parentFolder, **kwargs):
        """create a folder in a specified course"""
        folder = self.canvasapi.course.create_folder(
            courseID, folderName, parent_folder_path=parentFolder, **kwargs
        )
        return folder

    def getSyllabus(self, courseID):
        """Finds the syllabus in a course, downloads it locally,
        and returns the file name
        """
        files = self.getFilesData(courseID)
        for file in files:
            fileName = file.get("display_name")
            if "syllabus" in fileName.lower():
                url = file.get("url")
                wget.download(url)
                return fileName
        return None

    # ---PAGES------------------------------------------------------------------

    def getPagesData(self, courseID, **kwargs):
        """returns a list of pages data for a course"""
        response = self.canvasapi.course.get_pages(courseID, **kwargs)
        pages = depaginate(response)
        return pages

    def getPages(self, courseID, **kwargs):
        """returns a list of page model objects"""
        response = self.canvasapi.course.get_pages(courseID, **kwargs)
        itemList = []
        for item in response:
            item = Page(item)
            itemList.append(item)
        return itemList

    def getPageContent(self, courseID, pageURLorID, **kwargs):
        """retrieve the content of a course wiki page"""
        response = self.canvasapi.course.get_page(courseID, pageURLorID, **kwargs)
        return response

    def createPage(self, courseID, pageTitle, pageContent, **kwargs):
        """create a new wiki page for a course"""
        wikiPage = {"title": pageTitle, "body": pageContent, "published": "true"}
        return self.canvasapi.course.create_page(courseID, wikiPage, **kwargs)

    def convertPageToFile(self, courseID, pageURLorID, fileType="docx"):
        """Convert the contents of a Canvas page to a file.
        Default file type is .docx. Currently only supports this file type.
        """
        pageContent = self.getPageContent(courseID, pageURLorID)
        file = canvasFunctions.pages.getFileContent(pageContent, fileType)
        return file

    # ---ASSIGNMENTS------------------------------------------------------------

    def getAssignmentsData(self, courseID, **kwargs):
        """returns a list of assignments data for a course"""
        response = self.canvasapi.course.get_assignments(courseID, **kwargs)
        return response.json()

    def getAssignments(self, courseID, **kwargs):
        """returns a list of assignment model objects"""
        response = self.canvasapi.course.get_assignments(courseID, **kwargs)
        itemList = []
        for item in response:
            assignment = Assignment(item)
            itemList.append(assignment)
        return itemList

    def exportAssignmentListCSV(self, courseID, **kwargs):
        """Export a list of the course's assignments as a .csv file"""
        print(" inside export ")
        assignments = self.getAssignmentsData(courseID, **kwargs)
        if assignments is None:
            return "There was an error finding the assignments."

        return canvasFunctions.assignments.assignmentListCSV(assignments)

    def getAssignmentSubmissions(self, courseID, assignmentID, **kwargs):
        """Retrieves an assignment and its submissions from the Canvas API.
        Returns an Assignment model object.
        """
        response = self.canvasapi.course.get_assignment(courseID, assignmentID)
        assignment = Assignment(response)

        subPagList = self.canvasapi.assignment.get_submissions(courseID, assignmentID)
        submissions = depaginate(subPagList)
        assignment.setSubmissions(submissions)

        return assignment

    def downloadAssignmentSubmissionsCSV(self, courseID, assignmentID):
        """
        Exports all student submissions of a specified assignment as a .csv file
        """
        course = self.getCourse(courseID)
        users = self.getUsers(courseID)
        course.addUsers(users)
        assignment = self.getAssignmentSubmissions(courseID, assignmentID)

        return canvasFunctions.assignments.exportSubmissions(course, assignment)

    def submitAssignment(self, courseID, assignmentID, submission, file=None, **kwargs):
        self.canvasapi.assignment.submit(
            courseID, assignmentID, submission, file=file, **kwargs
        )

    # ---QUIZZES----------------------------------------------------------------

    def getQuizzesData(self, courseID, **kwargs):
        """returns a list of quizzes data for a course"""
        response = self.canvasapi.course.get_quizzes(courseID, **kwargs)
        quizzes = depaginate(response)
        return quizzes

    def getQuizzes(self, courseID, **kwargs):
        """returns a list of quiz model objects"""
        response = self.canvasapi.course.get_quizzes(courseID, **kwargs)
        itemList = []
        for item in response:
            item = Quiz(item)
            itemList.append(item)
        return itemList

    def getQuizList(self, courseID):
        """returns a list of quiz names and ids for a given course"""
        quizzes = self.getQuizzesData(courseID)
        quizList = []
        for quiz in quizzes:
            entry = {"name": quiz.get("title"), "id": quiz.get("id")}
            quizList.append(entry)
        return quizList

    def exportQuizListCSV(self, courseID):
        """Export a list of the course's quizzes as a .csv file"""
        quizzes = self.getQuizzesData(courseID)
        if quizzes is None:
            return "There was an error downloading the quizzes."

        return canvasFunctions.quizzes.quizListCSV(quizzes)

    def getQuizSubmissions(self, courseID, quizID, **kwargs):
        """Retrieves a quiz and its submissions from the Canvas API.
        Returns an Quiz model object.
        """
        response = self.canvasapi.course.get_quiz(courseID, quizID, **kwargs)
        quiz = Quiz(response)

        subPagList = self.canvasapi.quiz.get_submissions(courseID, quizID)
        submissions = depaginate(subPagList)
        quiz.setSubmissions(submissions)

        return quiz

    def downloadQuizSubmissionsCSV(self, courseID, quizID):
        """Exports all student submissions for a
        specified quiz as a .csv file
        """
        course = self.getCourse(courseID)
        users = self.getUsers(courseID)
        course.addUsers(users)
        quiz = self.getQuizSubmissions(courseID, quizID)

        return canvasFunctions.quizzes.exportQuizSubmissions(course, quiz)

    # ------------------Author:KARAN CHOPRA--------------------------QTI Quiz IMPORT and EXPORT-------------------------------------------------

    # this function will convert the file into QTI format
    # and then call the Canvas Api to add a newQuiz in a course
    def importQuizFromQTI(self, courseId, file, quizName):
        text_content = file.read().decode("utf-8")
        qti_content = generate_qti_quiz(text_content)
        # this will add the qti file as a new quiz
        result = self.canvasapi.course.import_qti_quiz(courseId, quizName, qti_content)
        return result

    # downloads a QTI quiz froma course
    def export_QTIQuiz(self, quizId, courseId):
        result = self.canvasapi.course.export_qti_quiz(courseId, quizId)
        return result

    # downloads all quiz from a course
    def exportEveryQti(self, courseId):
        result = self.canvasapi.course.export_All_Qti(courseId)
        return result

    def exportQuizzesToQTI(self, courseId, courseOption, quizType):
        """Export quizzes in QTI format from a specified course.
        This is a highly simplified placeholder.
        Actual implementation would depend on how your system stores
        quizzes and how they can be converted to QTI format.
        """
        quizzes = self.getQuizzesData(
            courseId, courseOption=courseOption, quizType=quizType
        )
        if not quizzes:
            return "failure"

        # Assume a function exists to convert quizzes to QTI and save/export them
        result = self.canvasapi.course.convert_quizzes_to_qti_and_export(quizzes)

        if result == "success":
            return "success"
        else:
            return "failure"

    # ---SETTINGS---------------------------------------------------------------

    def getSettings(self, courseID):
        """retrieves the settings and navigation tabs from Canvas and returns
        them as dictionaries
        """
        settings = self.canvasapi.course.get_settings(courseID)
        tabPagList = self.canvasapi.course.get_tabs(courseID)
        tabs = depaginate(tabPagList)
        return (settings, tabs)

    def importSettingsFromCourse(self, exportCourseID, importCourseID):
        """
        exports settings and navigation tabs from one course and directly
        imports them into another course
        """
        settings, tabs = self.getSettings(exportCourseID)

        response = self.canvasapi.course.update_settings(importCourseID, **settings)
        if response == "Error":
            return "Error"

        return canvasFunctions.settings.importNavigation(
            tabs, importCourseID, self.canvasapi
        )

    def exportSettingsToFile(self, courseID):
        """
        Exports course settings and navigation (tabs) to json files
        """
        course = self.getCourse(courseID)
        settings, tabs = self.getSettings(courseID)

        return canvasFunctions.settings.toFile(course, settings, tabs)

    def importSettingsFromFiles(self, courseID, settingsFile, navFile):
        """Imports course and navigation (tabs) settings from files"""
        return canvasFunctions.settings.fromFiles(
            courseID, settingsFile, navFile, self.canvasapi
        )

    # ------------------------------------------------------------------------------
    ### Pooja's additions
    # ------------------------------------------------------------------------------
    # -------------COURSE---------------------------------------------------------------
    def listDistinctRoles(self):
        """Retrieves distinct roles in the enrolled courses
        Returns a List of distinct roles
        """
        courses = self.canvasapi.course.get_courses()
        try:
            if courses.status_code == 200:
                distinct_roles = []
                courses = courses.json()
                for course in courses:
                    if "access_restricted_by_date" in course:
                        continue
                    enrollment = course.get("enrollments")
                    if (
                        enrollment is not None
                        and enrollment[0]["type"].title() not in distinct_roles
                    ):
                        if (
                            enrollment[0]["type"] == "ta"
                            and enrollment[0]["type"].upper() not in distinct_roles
                        ):
                            distinct_roles.append(enrollment[0]["type"].upper())
                            continue
                        distinct_roles.append(enrollment[0]["type"].title())
                return distinct_roles
            else:
                return self.canvasapi.course._requester.handleException(courses)
        except Exception as ex:
            return self.canvasapi.course._requester.handleException(courses)

    def getTerms(self):
        """
        Retrieves course registrations
        Returns a List of distinct course terms
        """
        courses = self.canvasapi.course.get_courses(
            include=["syllabus_body", "term", "favorites"]
        )
        if courses.status_code != 200:
            return self.canvasapi.course.handleException(courses)
        else:
            course_terms = []
            courses = courses.json()
            for course in courses:
                if "access_restricted_by_date" in course:
                    continue
                if course.get("term") is not None:
                    course_details = {
                        "id": course.get("id"),
                        "name": course.get("name"),
                        "term": course.get("term").get("name"),
                        "role": course.get("enrollments")[0]["type"],
                        "is_favorite": course.get("is_favorite"),
                    }
                course_terms.append(course_details)
            return course_terms

    def getCourseNames(self):
        """
        Retrieves course information that the user has enrolled in
        Returns a List of course Names
        """
        courses = self.canvasapi.course.get_courses()
        if courses.status_code != 200:
            return self.canvasapi.course.handleException(courses)
        courseNameList = []
        for course in courses.json():
            if "access_restricted_by_date" not in course:
                courseNameList.append(course["name"])
        return courseNameList

    def getCourseNamesID(self):
        """
        Retrieves course information that the user has enrolled in
         Returns a List of courses with their names and IDs
        """
        courses = self.canvasapi.course.get_courses()
        if courses.status_code != 200:
            return self.canvasapi.course.handleException(courses)
        courseNameAndIDList = []
        for course in courses.json():
            if "access_restricted_by_date" not in course:
                course_info = {"id": course["id"], "name": course["name"]}
            courseNameAndIDList.append(course_info)

        return courseNameAndIDList

    # -------SUBMISSION AND SUPPORTED APIS--------------------------------------------------------------
    def getAssignmentMetadata(self, request):
        """
        Retrieves submission details for an assignment
        :param request : UI request having course Id and assignment Ids
        :type request  : JSON
        Returns dictionary having metdata about the assignment such as allowed extensions, acceptable file types
        """
        try:
            response = self.canvasapi.assignment.getAssignmentMetadata(
                request, inlclude=["submission"]
            )
            if response.status_code != 200:
                return json.loads(response.text)
            else:
                response = response.json()
                if "allowed_extensions" in response:
                    entity = {
                        "submission_types": response["submission_types"],
                        "allowed_extensions": response["allowed_extensions"],
                    }
                    return entity
                else:
                    entity = {"submission_types": response["submission_types"]}
                    return entity
        except Exception as e:
            return "Exception while fetching assignment metadata"

    def getSubmitterData(self):
        """
        Retrieves submission details for an assignment
        Returns dictionary having metdata about the assignment such as allowed extensions, acceptable file types
        """
        try:
            submitterData = self.canvasapi.assignment.getSubmitterData()
            if submitterData.status_code != 200:
                return json.loads(submitterData.text)
            else:
                return submitterData.json()
        except Exception as e:
            return "Could not fetch submitter data"

    def getCourseStudents(self, request):
        """
        Retrieves submission details for an assignment
        Returns dictionary having metdata about the assignment such as allowed extensions, acceptable file types
        """
        try:
            courseId = request["courseId"]
            students = self.canvasapi.course.getCourseStudents(courseId)

            submitterData = self.canvasapi.assignment.getSubmitterData()
            if submitterData.status_code != 200:
                return json.loads(submitterData.text)

            if students.status_code != 200:
                return json.loads(students.text)
            else:
                studentList = []
                for student in students.json():
                    # skip test students
                    if (
                        student["id"] == 4340916
                        or student["id"] == submitterData.json()["id"]
                    ):
                        continue
                    entity = {"name": student["name"], "studentId": student["id"]}
                    studentList.append(entity)
                return studentList
        except Exception as e:
            return "Could not fetch submitter data"

    def listAssignments(self, request):
        """
        Lists avaialble assignments for a course
        :param request : UI request having course Id and assignment Ids
        :type request  : JSON
        Returns List of Assignments
        """
        try:
            courseId = request["courseId"]
            asssignments = self.canvasapi.course.get_assignments(
                courseId, perpage="50", include=["syllabus_body", "term", "favorites"]
            )
            if asssignments.status_code != 200:
                return json.loads(asssignments.text)
            else:
                assignmentsList = []
                for assignment in asssignments.json():
                    if not assignment["is_quiz_assignment"]:
                        entity = {
                            "id": assignment["id"],
                            "courseId": assignment["course_id"],
                            "name": assignment["name"],
                        }
                        assignmentsList.append(entity)
                return assignmentsList
        except Exception as e:
            return "Could not fetch the assignments"

    def uploadSubmissionFiles(self, request, file):
        """
        Uploads the file to the temparary storage in order to fetch the FileId that is used in submission api
        :param request : UI request having course Id and assignment Ids
        :type request  : JSON
        :param file : File to be uploaded
        :type file  : File
        returns fileId after the successfull upload
        """
        try:
            upload_response = self.canvasapi.submission.uploadSubmissionFiles(
                request, file
            )

            if upload_response.status_code != 200:
                return json.loads(upload_response.text)
            else:
                return upload_response.json()["id"]
        except Exception as e:
            return {"error": "Could not upload the file to the canvas"}

    def submitAnAssignment(self, request):
        """
        Submits the assignment
        :param request : UI request having course Id and assignment Ids
        :type request  : JSON
        returns state of submission
        """
        try:
            submissionResponse = self.canvasapi.submission.submitAnAssignment(request)
            if (
                submissionResponse.status_code != 200
                and submissionResponse.status_code != 201
            ):
                return json.loads(submissionResponse.text)
            else:
                submissionResponse = submissionResponse.json()
                if len(request["contributors"]) > 0:
                    memberUpdation = (
                        self.canvasapi.submission.updateCommentsForContributors(request)
                    )
                    if "errors" in memberUpdation.json():
                        # Errors during updation
                        return self.canvasapi._requester.handleException(memberUpdation)
                db_action_state = self.canvasapi.database.update_submission_in_db(
                    request, submissionResponse
                )
                if (
                    "workflow_state" in submissionResponse
                    and db_action_state == "success"
                ):
                    return "The assignment is {}".format(
                        submissionResponse["workflow_state"]
                    )
                elif db_action_state == "error":
                    return "Error Occured while updating teh DB"
                else:
                    return submissionResponse
        except Exception as e:
            print(" Exception while submitting an assignment")

    # -------EXPORT COLLABORATORS--------------------------------------------------------------
    def exportTeamfrmCmts(self, request):
        """
        Exports the contributors details in an csv file
        :param request : UI request having course Id and assignment Ids
        :type request  : JSON
        returns status of the file download
        """
        try:
            teams_info = []
            # submissions : A list in which each elelment belongs to each submitter having submission comments associated
            submissions = self.canvasapi.submission.getSubmissions(request)

            if submissions.status_code != 200:
                return json.loads(submissions.text)
            else:
                for submission in submissions.json():
                    membersData = []
                    # submission by Test student to be ignored
                    if submission["user"]["id"] == 4340916:
                        continue
                    # single submitter details
                    submissionDetail = self.populateStudentInfo(request, submission)
                    # ensures there is atleast one submission comment
                    # sorts comments based on creation date : latest comment will have the updated group information
                    # latest comment could be by the instructor/TA and hence filter comment based on author id
                    # filters comments by the submitter
                    # submitter comment will be having unwanted  hyphers and characters hence extracting group data
                    # print("submission comments and len ", len(submission['submission_comments']),submission['submission_comments'] )
                    # if (len(submission['submission_comments']) > 0 and submission['workflow_state'] == 'submitted' ):
                    #     print(" tehre is comment ")

                    contributors = self.canvasapi.database.get_contributors_from_db(
                        submission["id"]
                    )
                    if len(contributors) > 0:
                        if contributors[0] != "":
                            print(" contributors", contributors)
                            # fetches additional data about the members with their name and id
                            membersData = (
                                self.canvasapi.submission.getContributorDetails(
                                    contributors
                                )
                            )
                            if "errors" in membersData:
                                return membersData
                            else:
                                membersData.append(
                                    [
                                        submissionDetail["submitter_name"],
                                        submissionDetail["submitter_canvas_id"],
                                        submissionDetail["submitter_login_id"],
                                        "submitter",
                                    ]
                                )
                                submissionDetail["membersData"] = membersData
                        else:
                            membersData.append(
                                [
                                    submissionDetail["submitter_name"],
                                    submissionDetail["submitter_canvas_id"],
                                    submissionDetail["submitter_login_id"],
                                    "submitter",
                                ]
                            )
                            submissionDetail["membersData"] = membersData

                    teams_info.append(submissionDetail)
                assignment = self.canvasapi.assignment.getAssignmentName(request)
                if assignment.status_code != 200:
                    return json.loads(assignment.text)
                status = self.canvasapi.collaboration.exportToCSV(
                    teams_info, assign_name=assignment.json().get("name")
                )
            return status
        except Exception as ex:
            print(
                " Error occured while exporting group information from the comments ",
                ex,
            )

    def populateStudentInfo(self, request, submission):
        """
        constructs a dictory having the necessary information extracted from the single submission
        :param request : UI request having course Id and assignment Ids
        :type request  : JSON
        :param submission : a single assignment submission
        :type submission  : JSON
        returns dictionary
        """
        return {
            "canvas_assignment_id": str(request["assignId"]),
            "submission_id": submission["id"],
            "submission_status": submission["workflow_state"],
            "submitter_name": submission["user"]["name"],
            "submitter_canvas_id": submission["user"]["id"],
            "submitter_login_id": submission["user"]["login_id"],
        }

    # -----------EXPORT SYLLABUS and SUPPORTED APIS-------------------------------------------------------------------
    def exportSyllabusToPdf(self, request):
        """
        Exports the Syllabus into a pdf file or a zip file if multiple export is enabled
        :param request : UI request with either single course syllabus export or multiple export
        :type request  : JSON
        returns None
        """
        courseId = request["courseId"]
        isSaveAll = request["isSaveAll"]
        if isSaveAll:
            files = []
            courses = self.canvasapi.course.get_courses()
            if courses.status_code != 200:
                return json.loads(courses.text)
            else:
                for course in courses.json():
                    if "access_restricted_by_date" in course:
                        continue
                    syllabusPage = {}
                    syllabusPage["course"] = course
                    assignments = self.listAssignmnets(courseId=str(course["id"]))
                    if "errors" in assignments:
                        return json.loads(assignments.text)
                    else:
                        syllabusPage["assignments"] = assignments
                        file_name = self.canvasapi.file.generatePdfFile(syllabusPage)
                        if file_name is not None:
                            files.append(file_name)
                self.canvasapi.file.zipFiles(files)
        else:
            course = self.canvasapi.course.get_course(courseId=courseId)
            if course.status_code != 200:
                return json.loads(course.text)
            else:
                course = course.json()
                syllabusPage = {}
                syllabusPage["course"] = course
                assignments = self.listAssignmnets(courseId=courseId)
                if "errors" in assignments:
                    return json.loads(assignments.text)
                else:
                    syllabusPage["assignments"] = assignments
                self.canvasapi.file.generatePdfFile(syllabusPage)

    def listAssignmnets(self, courseId):
        """
        Fetches list of assignments for a given course Id
        :param courseId : Course Id of the course
        :type courseId  : string
        returns list of assignments
        :return type: dict
        """
        assignments = self.canvasapi.assignment.listAssignmnets(courseId=courseId)
        if assignments.status_code != 200:
            return assignments
        else:
            # assignments = sorted([assignmnet for assignmnet in assignments.json() if assignmnet["due_at"] is not None], key=lambda assignmnet: (datetime.strptime(assignmnet['due_at'], '%Y-%m-%d')))
            assignmnet_info = {}
            for assignment in assignments.json():
                if assignment["due_at"] is not None:
                    assignment["due_at"] = assignment["due_at"][:10]
                assignmnet_info[assignment["name"]] = [
                    assignment["html_url"],
                    assignment["due_at"],
                    assignment["points_possible"],
                ]
            return assignmnet_info

    def getSyllabusbody(self, courseId):
        """
        Fetches list of assignments for a given course Id
        :param courseId : Course Id of the course
        :type courseId  : string
        returns list of assignments
        :return type: dict
        """
        course = self.canvasapi.course.get_course(courseId=str(courseId))
        if course.status_code != 200:
            return json.loads(course.text)
        else:
            return course.json()["syllabus_body"]


if __name__ == "__main__":
    canvas_services.main()

# -----------------------------------------------------------------------------------------------------------------------------------
