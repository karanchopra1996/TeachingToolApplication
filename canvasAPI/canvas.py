from .assignment import Assignment
from .collaboration import Collaboration
from .course import Course
from .file import File
from .folder import Folder
from .group import Group
from .module import Module
from .page import Page
from .quiz import Quiz
from .submission import Submission
from .requester import Requester
from .user import User
from .database import Database


class Canvas(object):
   """
   The main class to be instantiated to provide access to Canvas's API.
   """

   def __init__(self, base_url, canvas_headers):
      """
      :param base_url: The base URL of the Canvas instance's API.
      :type base_url: str
      :param access_token: The API key to authenticate requests with.
      :type access_token: json
      """

      # Ensure that the user-supplied access token and base_url contain no leading or
      # trailing spaces that might cause issues when communicating with the API.
      base_url = base_url.strip()

      self._requester = Requester(base_url, canvas_headers)

      # Interface instances
      self.assignment = Assignment(self._requester)
      self.collaboration = Collaboration(self._requester)
      self.course = Course(self._requester)
      self.file = File(self._requester)
      self.folder = Folder(self._requester)
      self.group = Group(self._requester)
      self.module = Module(self._requester)
      self.page = Page(self._requester)
      self.quiz = Quiz(self._requester)
      self.submission = Submission(self._requester)
      self.user = User(self._requester)
      self.database = Database(self._requester)

   # # Option to get a new instance of a canvas api subclass
   # def assignmentAPI(self):
   #    """ 
   #    Returns a new instance of :class:'canvasAPI.Assignment'.
   #    Provides the interface for assignment related API calls.
   #    """
   #    return Assignment(self._requester)

   # def collaborationAPI(self):
   #    """ 
   #    Returns a new instance of :class:'canvasAPI.Collaboration'.
   #    Provides the interface for collaboration related API calls.
   #    """
   #    return Collaboration(self._requester)

   # def courseAPI(self):
   #    """ 
   #    Returns a new instance of :class:'canvasAPI.Course'.
   #    Provides the interface for course related API calls.
   #    """
   #    course = Course(self._requester)
   #    return course

   # def fileAPI(self):
   #    """ 
   #    Returns a new instance of :class:'canvasAPI.File'.
   #    Provides the interface for file related API calls.
   #    """
   #    return File(self._requester)

   # def folderAPI(self):
   #    """ 
   #    Returns a new instance of :class:'canvasAPI.Folder'.
   #    Provides the interface for folder related API calls.
   #    """
   #    return Folder(self._requester)

   # def groupAPI(self):
   #    """ 
   #    Returns a new instance of :class:'canvasAPI.Group'.
   #    Provides the interface for group related API calls.
   #    """
   #    return Group(self._requester)

   # def moduleAPI(self):
   #    """ 
   #    Returns a new instance of :class:'canvasAPI.Module'.
   #    Provides the interface for module related API calls.
   #    """
   #    return Module(self._requester)

   # def pageAPI(self):
   #    """ 
   #    Returns a new instance of :class:'canvasAPI.Page'.
   #    Provides the interface for page related API calls.
   #    """
   #    return Page(self._requester)
   
   # def quizAPI(self):
   #    """ 
   #    Returns a new instance of :class:'canvasAPI.Quiz'.
   #    Provides the interface for quiz related API calls.
   #    """
   #    return Quiz(self._requester)

   # def submissionAPI(self):
   #    """ 
   #    Returns a new instance of :class:'canvasAPI.Submission'.
   #    Provides the interface for submission related API calls.
   #    """
   #    return Submission(self._requester)
   
   # def userAPI(self):
   #    """ 
   #    Returns a new instance of :class:'canvasAPI.User'.
   #    Provides the interface for user related API calls.
   #    """
   #    return User(self._requester)

