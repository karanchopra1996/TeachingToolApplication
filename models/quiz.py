from models.modelObject import ModelObject

class Quiz(ModelObject):
   def __init__(self, data):
      super(Quiz, self).__init__(data)
      self.id = data.get('id')
      self.title = data.get('title')
      self.submissions = []

      self.users = {} # dictionary of quiz takers {user_id: user_name}

   def addUser(self, user):
      self.users.update(user)

   def findUser(self, userID):
      return self.users.get(userID)

   def setSubmissions(self, data):
      self.submissions = data

   def getSubmissions(self):
      return self.submissions

# class QuizSubmission(ModelObject):
#    def __init__(self, data):
#       super(QuizSubmission, self).__init__(data)
   