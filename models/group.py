from models.modelObject import ModelObject

class Group(ModelObject):
   def __init__(self, data):
      super(Group, self).__init__(data)
      self.id = data.get('id')
      self.name = data.get('name')
      self.members = []

   def addMember(self, member):
      self.members.append(member)
   
   def getMembers(self):
      return self.members

   def setCategoryName(self, groupCategory):
      self.data['group_category_name'] = groupCategory.get('name')
   

class GroupCategory(ModelObject):
   def __init__(self, data):
      super(GroupCategory, self).__init__(data)
      self.id = data.get('id')
      self.name = data.get('name')
      self.groupsById = {}
      self.groupsByName = {}

   def addGroup(self, group):
      self.groupsById[group.id] = group
      self.groupsByName[group.name] = group
   
   def getGroup(self, groupIdOrName):
      """ return a group by ID or by name """
      if isinstance(groupIdOrName, int):
         return self.groupsById.get(groupIdOrName)
      
      return self.groupsByName.get(groupIdOrName)

   def getGroups(self):
      return self.groupsById.values()

