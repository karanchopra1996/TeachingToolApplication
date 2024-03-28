from models.modelObject import ModelObject

class Assignment(ModelObject):
   def __init__(self, data):
      super(Assignment, self).__init__(data)
      self.id = data.get('id')
      self.name = data.get('name')
      self.submissions = []

   def setSubmissions(self, data):
      self.submissions = data

   def getSubmissions(self):
      return self.submissions