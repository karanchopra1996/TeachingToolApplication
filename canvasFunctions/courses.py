

def getCourseDetails(courses):
    details = []
    for course in courses:
        if course.get('name') is not None:
            entity = {'id':course['id'],
                    'name':course['name'], 
                    'term':course['term']['name'], 
                    'role':course['enrollments'][0]['type'],
                    'is_favorite':course['is_favorite']}
            details.append(entity)
    return details

#Gets all the distinct roles for the current logged in user 
def listDistinctRoles(courses):
    """ Returns a list of all the distinct roles for the current user """
    distinct_roles = []
    for course in courses:
        # use course.get('{key}') instead of course['{key}'] in case user does not
        # have access to course data
        enrollment = course.get('enrollments')
        if enrollment is not None:  # if access is not allowed, it will return None
            for firstenrollment in enrollment:
                type = firstenrollment.get('type')
                if type.title() not in distinct_roles:
                    if type == 'ta':
                        distinct_roles.append(type.upper())
                        continue
                    distinct_roles.append(type.title())
    return distinct_roles