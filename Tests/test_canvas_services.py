import json
import pytest

from core.canvas_services import canvas_services
from canvasAPI.assignment import Assignment
from canvasAPI.course import Course
from canvasAPI.group import Group
from canvasAPI.quiz import Quiz
from canvasAPI.requester import Requester
from canvasAPI.exceptions import ResourceDoesNotExist

from models.assignment import Assignment as assignmentModel
from models.course import Course as courseModel
from models.folder import File as fileModel
from models.folder import Folder as folderModel
from models.group import Group as groupModel
from models.group import GroupCategory
from models.page import Page as pageModel
from models.quiz import Quiz as quizModel
from models.user import User as userModel

BASE_URL = "https://example.com/api/v1/"
API_KEY = "123"
# canvas = canvas_services(BASE_URL, API_KEY)

COURSE_ID = 1
DATA_FILE = "Tests/resources/mock_data.json"

@pytest.fixture
def canvas():
   """ Return an instance of :class: `Canvas` that doesn't make real requests """

   _canvas = canvas_services(BASE_URL, API_KEY)

   yield _canvas

def getDictSubset(data, keys):
   subset = {key: data.get(key) for key in keys}
   return subset

# ---COURSES--------------------------------------------------------------------

def test_get_course_data(mocker, canvas, json_loader):
   testData = json_loader("Tests/resources/mock_data.json", "course_good")
   mockData = testData.get('data')
   get_mock = mocker.MagicMock()
   get_mock.json.return_value = testData.get('data')
   get_mock.status_code = testData.get('status_code')
   request_mock = mocker.patch.object(Requester, '_get_request', return_value=get_mock)

   response = canvas.getCourseData(1)
   assert response == mockData

def test_get_course_data_bad_id(mocker, canvas):
   get_mock = mocker.MagicMock()
   get_mock.json.return_value = None
   get_mock.status_code = 404
   request_mock = mocker.patch.object(Requester, '_get_request', return_value=get_mock)

   with pytest.raises(ResourceDoesNotExist):
      canvas.getCourseData(1)

def test_get_course(mocker, canvas, json_loader):
   mockData = json_loader(DATA_FILE, "course")
   courseID = mockData.get('id')
   mocker.patch.object(Course, 'get_course', return_value=mockData)

   result = canvas.getCourse(courseID)
   assert type(result) is courseModel

def test_get_courses_all_data(mocker, canvas, json_loader):
   mockData = json_loader(DATA_FILE, "courses")
   # get_mock = mocker.MagicMock()
   # get_mock.json.return_value = mockData
   # get_mock.status_code = 200
   mocker.patch.object(Course, 'get_courses', return_value=mockData)

   response = canvas.getCourses()
   assert response == mockData

def test_get_courses_subset(mocker,canvas, json_loader):
   mockData = json_loader(DATA_FILE, "courses")
   subset = ['name', 'id']
   mockReturn = []
   for item in mockData:
      mockReturn.append(getDictSubset(item, subset))
   mocker.patch.object(Course, 'get_courses', return_value=mockData)

   response = canvas.getCourses(subset)
   assert response == mockReturn

def test_get_favorites_all_data(mocker, canvas, json_loader):
   mockData = json_loader(DATA_FILE, "courses")
   mocker.patch.object(Course, 'get_favorites', return_value=mockData)

   response = canvas.getFavorites()
   assert response == mockData

def test_get_favorites_subset(mocker,canvas, json_loader):
   mockData = json_loader(DATA_FILE, "courses")
   subset = ('name', 'id')
   mockReturn = []
   for item in mockData:
      mockReturn.append(getDictSubset(item, subset))
   mocker.patch.object(Course, 'get_favorites', return_value=mockData)

   response = canvas.getFavorites(subset)
   assert response == mockReturn

# ---STUDENTS-------------------------------------------------------------------

def test_get_students_data(mocker, canvas, json_loader):
   mockData = json_loader(DATA_FILE, "students")
   mocker.patch.object(Course, 'get_users', return_value=mockData)

   response = canvas.getStudentsData(COURSE_ID)
   assert response == mockData

def test_get_students(mocker, canvas, json_loader):
   mockData = json_loader(DATA_FILE, "students")
   mocker.patch.object(Course, 'get_users', return_value=mockData)

   result = canvas.getStudents(COURSE_ID)
   assert len(result) == len(mockData)
   assert type(result[0]) is userModel

def test_get_users(mocker, canvas, json_loader):
   mockData = json_loader(DATA_FILE, "users")
   mocker.patch.object(Course, 'get_users', return_value=mockData)

   result = canvas.getStudents(COURSE_ID)
   assert len(result) == len(mockData)
   assert type(result[0]) is userModel

def test_export_students(mocker, canvas, json_loader):
   mockCourse = json_loader(DATA_FILE, "course")
   courseID = mockCourse.get('id')
   mocker.patch.object(Course, 'get_course', return_value=mockCourse)

   mockStudents = json_loader(DATA_FILE, "students")
   mocker.patch.object(Course, 'get_users', return_value=mockStudents)

   correctOutput = json_loader(DATA_FILE, "export_students_default")

   result = canvas.exportStudents(courseID)
   assert result == correctOutput

def test_export_students_key(mocker, canvas, json_loader):
   mockCourse = json_loader(DATA_FILE, "course")
   courseID = mockCourse.get('id')
   mocker.patch.object(Course, 'get_course', return_value=mockCourse)

   mockStudents = json_loader(DATA_FILE, "students")
   key = 'email'
   mocker.patch.object(Course, 'get_users', return_value=mockStudents)

   correctOutput = json_loader(DATA_FILE, "export_students_key")

   result = canvas.exportStudents(courseID, key)
   assert result == correctOutput

def test_export_course_roster(mocker, canvas, json_loader):
   mockCourse = json_loader(DATA_FILE, "course")
   courseID = mockCourse.get('id')
   mocker.patch.object(Course, 'get_course', return_value=mockCourse)

   mockStudents = json_loader(DATA_FILE, "students")
   mocker.patch.object(Course, 'get_users', return_value=mockStudents)

   result = canvas.exportCourseRoster(courseID)
   assert result == 'success'

 # ---GROUPS--------------------------------------------------------------------

def test_get_groups_data(mocker, canvas, json_loader):
   mockData = json_loader(DATA_FILE, "groups")
   mocker.patch.object(Course, 'get_groups', return_value=mockData)

   response = canvas.getGroupsData(COURSE_ID)
   assert response == mockData

def test_get_groups(mocker, canvas, json_loader):
   mockData = json_loader(DATA_FILE, "groups")
   mocker.patch.object(Course, 'get_groups', return_value=mockData)

   result = canvas.getGroups(COURSE_ID)
   assert len(result) == len(mockData)
   assert type(result[0]) is groupModel

def test_get_groups_categories(mocker, canvas, json_loader):
   mockCategories = json_loader(DATA_FILE, "group_categories")
   mocker.patch.object(Course, 'get_group_categories', return_value=mockCategories)

   mockGroups = json_loader(DATA_FILE, "groups")
   mockGroup1 = mockGroups[:2]
   mockGroup2 = mockGroups[2:]
   mocker.patch.object(Group, 'get_groups_in_category', side_effect=[mockGroup1, mockGroup2])

   result = canvas.getGroupsCategories(COURSE_ID)

   assert len(result) == len(mockCategories)
   assert type(result[0]) is GroupCategory
   assert len(result[0].getGroups()) == len(mockGroup1)
   resultGroup1 = result[0].getGroup(1)
   assert type(resultGroup1) is groupModel

def test_get_groups_list(mocker, canvas, json_loader):
   mockData = json_loader(DATA_FILE, "groups")
   mocker.patch.object(Course, 'get_groups', return_value=mockData)

   correctOutput = json_loader(DATA_FILE, "get_groups_list")

   result = canvas.getGroupsList(COURSE_ID)
   assert result == correctOutput

def test_get_group_members(mocker, canvas, json_loader):
   mockCourse = json_loader(DATA_FILE, "course")
   courseID = mockCourse.get('id')
   mocker.patch.object(Course, 'get_course', return_value=mockCourse)

   mockStudents = json_loader(DATA_FILE, "students")
   mocker.patch.object(Course, 'get_users', return_value=mockStudents)

   mockGroups = json_loader(DATA_FILE, "groups")
   mocker.patch.object(Course, 'get_groups', return_value=mockGroups)

   mocker.patch.object(Group, 'get_users', return_value=mockStudents)
   
   mockCategories = json_loader(DATA_FILE, "group_categories")
   mockCat1 = mockCategories[0]
   mockCat2 = mockCategories[1]
   mockCatList = [mockCat1, mockCat1, mockCat2, mockCat2]
   mocker.patch.object(Group, 'get_group_category', side_effect=mockCatList)

   result = canvas.getGroupMembers(courseID, True)
   assert type(result) is courseModel
   assert len(result.getGroups()) == len(mockGroups)
   resultGroup1 = result.getGroup(1)
   assert type(resultGroup1) is groupModel
   resultMembers = resultGroup1.getMembers()
   assert len(resultMembers) == len(mockStudents)
   assert type(resultMembers[0]) is userModel

def test_export_groups_json(mocker, canvas, json_loader):
   mockCourse = json_loader(DATA_FILE, "course")
   courseID = mockCourse.get('id')
   mocker.patch.object(Course, 'get_course', return_value=mockCourse)

   mockStudents = json_loader(DATA_FILE, "students")
   mocker.patch.object(Course, 'get_users', return_value=mockStudents)

   mockGroups = json_loader(DATA_FILE, "groups")
   mocker.patch.object(Course, 'get_groups', return_value=mockGroups)

   mockGroup1 = mockStudents[:2]
   mockGroup2 = mockStudents[2:]
   mockGroup3 = mockStudents[::2]
   mockGroup4 = mockStudents[:1]
   mockGroupMembers = [mockGroup1, mockGroup2, mockGroup3, mockGroup4]
   mocker.patch.object(Group, 'get_users', side_effect=mockGroupMembers)

   correctOutput = json_loader(DATA_FILE, "export_groups_json")

   result = canvas.exportGroupsJSON(courseID)
   assert result == correctOutput

def test_export_groups_csv(mocker, canvas, json_loader):
   mockCourse = json_loader(DATA_FILE, "course")
   courseID = mockCourse.get('id')
   mocker.patch.object(Course, 'get_course', return_value=mockCourse)

   mockStudents = json_loader(DATA_FILE, "students")
   mocker.patch.object(Course, 'get_users', return_value=mockStudents)

   mockGroups = json_loader(DATA_FILE, "groups")
   mocker.patch.object(Course, 'get_groups', return_value=mockGroups)

   mocker.patch.object(Group, 'get_users', return_value=mockStudents)
   
   mockCategories = json_loader(DATA_FILE, "group_categories")
   mockCat1 = mockCategories[0]
   mockCat2 = mockCategories[1]
   mockCatList = [mockCat1, mockCat1, mockCat2, mockCat2]
   mocker.patch.object(Group, 'get_group_category', side_effect=mockCatList)

   result = canvas.exportGroupsCSV(courseID)
   assert result == 'success'

def test_get_group_members(mocker, canvas, json_loader):
   mockCourse = json_loader(DATA_FILE, "course")
   courseID = mockCourse.get('id')
   mocker.patch.object(Course, 'get_course', return_value=mockCourse)

   mockStudents = json_loader(DATA_FILE, "students")
   mocker.patch.object(Course, 'get_users', return_value=mockStudents)

   mockGroups = json_loader(DATA_FILE, "groups")
   mocker.patch.object(Course, 'get_groups', return_value=mockGroups)

   mocker.patch.object(Group, 'get_users', return_value=mockStudents)
   
   mockCategories = json_loader(DATA_FILE, "group_categories")
   mockCat1 = mockCategories[0]
   mockCat2 = mockCategories[1]
   mockCatList = [mockCat1, mockCat1, mockCat2, mockCat2]
   mocker.patch.object(Group, 'get_group_category', side_effect=mockCatList)

   result = canvas.getGroupMembers(courseID, True)
   assert type(result) is courseModel
   assert len(result.getGroups()) == len(mockGroups)
   resultGroup1 = result.getGroup(1)
   assert type(resultGroup1) is groupModel
   resultMembers = resultGroup1.getMembers()
   assert len(resultMembers) == len(mockStudents)
   assert type(resultMembers[0]) is userModel

def test_import_student_groups(mocker, canvas, json_loader):
   mockCourse = json_loader(DATA_FILE, "course")
   courseID = mockCourse.get('id')
   mocker.patch.object(Course, 'get_course', return_value=mockCourse)

   mockCategories = json_loader(DATA_FILE, "group_categories")
   mocker.patch.object(Course, 'get_group_categories', return_value=mockCategories)

   mockGroups = json_loader(DATA_FILE, "groups")
   mockGroup1 = mockGroups[:2]
   mockGroup2 = mockGroups[2:]
   mocker.patch.object(Group, 'get_groups_in_category', side_effect=[mockGroup1, mockGroup2])

   mocker.patch('canvasFunctions.students.importGroups', return_value='success')
   
   result = canvas.importStudentGroups(courseID, 'fakefile')
   assert result == 'success'

# ---FILE SYSTEM----------------------------------------------------------------

def test_get_folders_data(mocker, canvas, json_loader):
   mockFolders = json_loader(DATA_FILE, "folders")
   mocker.patch.object(Course, 'get_folders', return_value=mockFolders)
   
   result = canvas.getFoldersData(COURSE_ID)
   assert result == mockFolders

def test_get_folders(mocker, canvas, json_loader):
   mockFolders = json_loader(DATA_FILE, "folders")
   mocker.patch.object(Course, 'get_folders', return_value=mockFolders)

   result = canvas.getFolders(COURSE_ID)
   assert len(result) == len(mockFolders)
   assert type(result[0]) is folderModel

def test_get_folders_list(mocker, canvas, json_loader):
   mockFolders = json_loader(DATA_FILE, "folders")
   mocker.patch.object(Course, 'get_folders', return_value=mockFolders)

   correctOutput = json_loader(DATA_FILE, "get_folders_list")

   result = canvas.getFoldersList(COURSE_ID)
   assert result == correctOutput

def test_get_files_data(mocker, canvas, json_loader):
   mockFiles = json_loader(DATA_FILE, "files")
   mocker.patch.object(Course, 'get_files', return_value=mockFiles)
   
   result = canvas.getFilesData(COURSE_ID)
   assert result == mockFiles

def test_get_files(mocker, canvas, json_loader):
   mockFiles = json_loader(DATA_FILE, "files")
   mocker.patch.object(Course, 'get_files', return_value=mockFiles)

   result = canvas.getFiles(COURSE_ID)
   assert len(result) == len(mockFiles)
   assert type(result[0]) is fileModel

# ---PAGES----------------------------------------------------------------------

def test_get_pages_data(mocker, canvas, json_loader):
   mockData = json_loader(DATA_FILE, "pages")
   mocker.patch.object(Course, 'get_pages', return_value=mockData)
   
   result = canvas.getPagesData(COURSE_ID)
   assert result == mockData

def test_get_pages(mocker, canvas, json_loader):
   mockData = json_loader(DATA_FILE, "pages")
   mocker.patch.object(Course, 'get_pages', return_value=mockData)

   result = canvas.getPages(COURSE_ID)
   assert len(result) == len(mockData)
   assert type(result[0]) is pageModel

def test_get_page_contents(mocker, canvas, json_loader):
   mockData = json_loader(DATA_FILE, "pages")
   mockPage = mockData[0]
   mockURL = mockPage.get('url')
   mocker.patch.object(Course, 'get_page', return_value=mockPage)
   
   result = canvas.getPageContents(COURSE_ID, mockURL)
   assert result == mockPage

def test_create_page(mocker, canvas, json_loader):
   mockData = json_loader(DATA_FILE, "pages")
   mockPage = mockData[0]
   mocker.patch.object(Course, 'create_page', return_value=mockPage)
   
   result = canvas.createPage(COURSE_ID, mockPage)
   assert result == mockPage

# ---ASSIGNMENTS----------------------------------------------------------------

def test_get_assignments_data(mocker, canvas, json_loader):
   mockData = json_loader(DATA_FILE, "assignments")
   mocker.patch.object(Course, 'get_assignments', return_value=mockData)
   
   result = canvas.getAssignmentsData(COURSE_ID)
   assert result == mockData

def test_get_assignments(mocker, canvas, json_loader):
   mockData = json_loader(DATA_FILE, "assignments")
   mocker.patch.object(Course, 'get_assignments', return_value=mockData)

   result = canvas.getAssignments(COURSE_ID)
   assert len(result) == len(mockData)
   assert type(result[0]) is assignmentModel

def test_export_assignment_list_csv(mocker, canvas, json_loader):
   mockData = json_loader(DATA_FILE, "assignments")
   mocker.patch.object(Course, 'get_assignments', return_value=mockData)

   result = canvas.exportAssignmentListCSV(COURSE_ID)
   assert result == "Successfully downloaded all assignments."

def test_get_assignment_submissions(mocker, canvas, json_loader):
   mockData = json_loader(DATA_FILE, "assignments")
   mockAssignment = mockData[0]
   assignmentID = mockAssignment.get('id')
   mocker.patch.object(Course, 'get_assignment', return_value=mockAssignment)

   mockSubmissions = json_loader(DATA_FILE, "assignment_submissions")
   mocker.patch.object(Assignment, 'get_submissions', return_value=mockSubmissions)

   result = canvas.getAssignmentSubmissions(COURSE_ID, assignmentID)
   assert type(result) is assignmentModel
   assert len(result.getSubmissions()) == len(mockSubmissions)

def test_download_assignment_submissions_csv(mocker, canvas, json_loader):
   mockCourse = json_loader(DATA_FILE, "course")
   mocker.patch.object(Course, 'get_course', return_value=mockCourse)

   mockStudents = json_loader(DATA_FILE, "students")
   mocker.patch.object(Course, 'get_users', return_value=mockStudents)
   
   mockData = json_loader(DATA_FILE, "assignments")
   mockAssignment = mockData[0]
   assignmentID = mockAssignment.get('id')
   mocker.patch.object(Course, 'get_assignment', return_value=mockAssignment)

   mockSubmissions = json_loader(DATA_FILE, "assignment_submissions")
   mocker.patch.object(Assignment, 'get_submissions', return_value=mockSubmissions)

   result = canvas.downloadAssignmentSubmissionsCSV(COURSE_ID, assignmentID)
   assert result == "Successfully downloaded all submissions for assignment: Assignment_1_Test"

# ---QUIZZES--------------------------------------------------------------------

def test_get_quizzes_data(mocker, canvas, json_loader):
   mockData = json_loader(DATA_FILE, "quiz")
   mocker.patch.object(Course, 'get_quizzes', return_value=mockData)
   
   result = canvas.getQuizzesData(COURSE_ID)
   assert result == mockData

def test_get_quizzes(mocker, canvas, json_loader):
   mockData = json_loader(DATA_FILE, "quiz")
   mocker.patch.object(Course, 'get_quizzes', return_value=mockData)

   result = canvas.getQuizzes(COURSE_ID)
   assert len(result) == len(mockData)
   assert type(result[0]) is quizModel

def test_get_quiz_list(mocker, canvas, json_loader):
   mockData = json_loader(DATA_FILE, "quiz")
   mocker.patch.object(Course, 'get_quizzes', return_value=mockData)

   correctOutput = json_loader(DATA_FILE, "get_quiz_list")

   result = canvas.getQuizList(COURSE_ID)
   assert result == correctOutput

def test_export_quiz_list_csv(mocker, canvas, json_loader):
   mockData = json_loader(DATA_FILE, "quiz")
   mocker.patch.object(Course, 'get_quizzes', return_value=mockData)

   result = canvas.exportQuizListCSV(COURSE_ID)
   assert result == "Successfully downloaded quizzes."

def test_get_quiz_submissions(mocker, canvas, json_loader):
   mockData = json_loader(DATA_FILE, "quiz")
   mockQuiz = mockData[0]
   quizID = mockQuiz.get('id')
   mocker.patch.object(Course, 'get_quiz', return_value=mockQuiz)

   mockSubmissions = json_loader(DATA_FILE, "quiz_submissions")
   mocker.patch.object(Quiz, 'get_submissions', return_value=mockSubmissions)

   result = canvas.getQuizSubmissions(COURSE_ID, quizID)
   assert type(result) is quizModel
   assert len(result.getSubmissions()) == len(mockSubmissions)

def test_download_quiz_submissions_csv(mocker, canvas, json_loader):
   mockCourse = json_loader(DATA_FILE, "course")
   mocker.patch.object(Course, 'get_course', return_value=mockCourse)

   mockStudents = json_loader(DATA_FILE, "students")
   mocker.patch.object(Course, 'get_users', return_value=mockStudents)

   mockData = json_loader(DATA_FILE, "quiz")
   mockQuiz = mockData[0]
   quizID = mockQuiz.get('id')
   quizTitle = mockQuiz.get('title')
   mocker.patch.object(Course, 'get_quiz', return_value=mockQuiz)

   mockSubmissions = json_loader(DATA_FILE, "quiz_submissions")
   mocker.patch.object(Quiz, 'get_submissions', return_value=mockSubmissions)

   result = canvas.downloadQuizSubmissionsCSV(COURSE_ID, quizID)
   assert result == "Successfully downloaded all submissions for quiz: {}".format(quizTitle)

# ---SETTINGS-------------------------------------------------------------------

def test_get_settings(mocker, canvas, json_loader):
   mockSettings = json_loader(DATA_FILE, "settings")
   mocker.patch.object(Course, 'get_settings', return_value=mockSettings)

   mockTabs = json_loader(DATA_FILE, "tabs")
   mocker.patch.object(Course, 'get_tabs', return_value=mockTabs)

   resultSettings, resultTabs = canvas.getSettings(COURSE_ID)
   assert resultSettings == mockSettings
   assert resultTabs == mockTabs

def test_import_settings_from_course(mocker, canvas, json_loader):
   mockSettings = json_loader(DATA_FILE, "settings")
   mocker.patch.object(Course, 'get_settings', return_value=mockSettings)

   mockTabs = json_loader(DATA_FILE, "tabs")
   mocker.patch.object(Course, 'get_tabs', return_value=mockTabs)

   mocker.patch.object(Course, 'update_settings', return_value=mockSettings)

   mockTab1 = mockTabs[0]
   mockTab2 = mockTabs[1]
   mockTab3 = mockTabs[2]
   mocker.patch.object(Course, 'update_tab', side_effect=[mockTab1, mockTab2, mockTab3])
   
   result = canvas.importSettingsFromCourse(COURSE_ID, COURSE_ID)
   assert result == 'success'

def test_export_settings_to_file(mocker, canvas, json_loader):
   mockCourse = json_loader(DATA_FILE, "course")
   mocker.patch.object(Course, 'get_course', return_value=mockCourse)

   mockSettings = json_loader(DATA_FILE, "settings")
   mocker.patch.object(Course, 'get_settings', return_value=mockSettings)

   mockTabs = json_loader(DATA_FILE, "tabs")
   mocker.patch.object(Course, 'get_tabs', return_value=mockTabs)

   result = canvas.exportSettingsToFile(COURSE_ID)
   assert result == 'success'

def test_import_settings_from_files(mocker, canvas, json_loader):
   mockData = json_loader(DATA_FILE, "import_settings_json")
   courseID = mockData.get('courseId')
   settingsFilePath = mockData.get('settingsFile')
   navFilePath = mockData.get('navFile')
   settingsFile = open(settingsFilePath, 'rb')
   navFile = open(navFilePath, 'rb')

   mocker.patch.object(Course, 'update_settings', return_value=None)
   mocker.patch.object(Course, 'update_tab', return_value=None)

   result = canvas.importSettingsFromFiles(courseID, settingsFile, navFile)
   assert result == 'success'