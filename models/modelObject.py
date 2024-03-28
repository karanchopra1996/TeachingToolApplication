class ModelObject(object):
   """
   Base object for all model objects
   """
   
   def __init__(self, data):
      self.data = data

   def getSubset(self, keys):
      subset = [self.data.get(key) for key in keys]
      return subset
   
   def getDictSubset(self, keys):
      subset = {key: self.get(key) for key in keys}
      return subset

   def getData(self):
      return self.data

   def get(self, key):
      return self.data.get(key)

   def setAttr(self, attr):
      """ attr = {attr: value} """
      self.data.update(attr)