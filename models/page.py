from models.modelObject import ModelObject

class Page(ModelObject):
   def __init__(self, data):
      super(Page, self).__init__(data)
      self.page_id = data.get('page_id')
      self.title = data.get('title')