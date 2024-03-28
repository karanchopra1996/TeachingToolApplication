from models.modelObject import ModelObject

class Folder(ModelObject):
   def __init__(self, data):
      super(Folder, self).__init__(data)
      self.id = data.get('id')
      self.name = data.get('name')
      self.full_name = data.get('full_name')


class File(ModelObject):
   def __init__(self, data):
      super(File, self).__init__(data)
      self.id = data.get('id')
      self.name = data.get('name')