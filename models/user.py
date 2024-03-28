from models.modelObject import ModelObject

class User(ModelObject):
   def __init__(self, data):
      super(User, self).__init__(data)
      self.id = data.get('id')
      self.name = data.get('name')

   def __repr__(self):
      return repr('User Name: {}, User Id: {}'.format(self.name, self.id))
