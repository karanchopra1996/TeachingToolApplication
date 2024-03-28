from models.modelObject import ModelObject

class Course(ModelObject):
   """
   If name = None, access to this course is restricted
   """
   
   def __init__(self, data):
      super(Course, self).__init__(data)
      self.id = data.get('id')
      self.name = data.get('name')
      self.access = True
      self.students = {}
      self.users = {}
      self.groups = {}
      self.groupCategoriesById = {}
      self.groupCategoriesByName = {}
      self.quizzes = {}
      self.assignments = {}
      self.assignmentsData = []

      if self.name is None:
         self.access = False
   
   def __repr__(self):
      return repr('Course Name: {}, Course Id: {}'.format(self.name, self.id))

   def addStudent(self, student):
      self.students[student.id] = student
   
   def addStudents(self, students):
      for student in students:
         self.addStudent(student)

   def getStudents(self):
      return self.students.values()

   def getStudentById(self, studentID):
      return self.students.get(studentID)

   def addUser(self, user, **kwargs):
      self.users[user.id] = user
      if kwargs.get('enrollment_type') == 'student':
         self.addStudent(user)
   
   def addUsers(self, users):
      for user in users:
         self.addUser(user)

   def getUsers(self):
      return self.users.values()

   def getUserById(self, userID):
      return self.users.get(userID)
      
   def addGroup(self, group):
      self.groups[group.id] = group
   
   def getGroups(self):
      return self.groups.values()
   
   def getGroup(self, groupID):
      """ return a group by ID """
      return self.groups.get(groupID)

   def addGroupCategory(self, category):
      self.groupCategoriesById[category.id] = category
      self.groupCategoriesByName[category.name] = category
   
   def getGroupCategories(self):
      return self.groupCategoriesById.values()
   
   def getGroupCategory(self, categoryIdOrName):
      """ return a group category by ID or by name """
      if isinstance(categoryIdOrName, int):
         return self.groupCategoriesById.get(categoryIdOrName)
      
      return self.groupCategoriesByName.get(categoryIdOrName)

   def addQuiz(self, quiz):
      self.quizzes[quiz.id] = quiz
   
   def getQuizzes(self):
      return self.quizzes.values()

   def getQuizById(self, quizID):
      return self.quizzes.get(quizID)

   def addAssignment(self, assignment):
      self.assignments[assignment.id] = assignment
   
   def getAssignments(self):
      return self.assignments.values()

   def getAssignmentById(self, assignmentID):
      return self.assignments.get(assignmentID)

   def setAssignmentsData(self, assignmentsData):
      self.assignmentsData = assignmentsData
   
   def getAssignmentsData(self):
      return self.assignmentsData