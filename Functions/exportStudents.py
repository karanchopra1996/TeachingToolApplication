import requests, json
from flask import request, jsonify
import csv,os,sys
from pathlib import Path
from core.canvas_services import canvas_services as canvasCore

#-----------------------------------------------------------------------------------------------
#This is called to create a csv file of student groups in a course
def exportManager():
    response = request.get_json(force=True) #force=True removes the content type requirement
    courseId = response.get('course')

    course = canvasCore.getCoursesName(courseId) #Sends to the core

    if course != "Error":
        name = course.get('name')
        fileName = name + "-Groups.csv"

        writer = fileCreate(fileName)

        groups = canvasCore.getGroups(courseId)
        if groups != "Error":
            for group in groups:
                groupId = group.get('id')
                groupName = group.get('name')
                groupCategoryId = group.get('group_category_id')
                categoryName = getCategoryName(groupCategoryId)

                # make api call to get each groups members
                members = canvasCore.getGroupMembers(groupId)

                if len(members) != 0:
                    for member in members:
                        studentId = member.get('id')
                        writer.writerow([member.get('name'), str(
                            studentId), categoryName, groupName])
                else:
                    writer.writerow(["", "", categoryName, groupName])

            return jsonify(message="Created CSV", status_code=200)
        else:
            return jsonify(message="Failed", status_code=500)
    else:
        return jsonify(message="Failed", status_code=500)


#-----------------------------------------------------------------------------------------------
#Makes and API call to get the group category name
def getCategoryName(id):
    category = canvasCore.getGroupCategory(id)
    if category != "Error":
        return category.get('name')
    else:
        return category


# -----------------------------------------------------------------------------------------------
# returns the courses roster into list
def getCourseRoster(courseId, key='name'):
    students = canvasCore.getCourseRoster(courseId)
    if students == "Error":
        return "Course was Not Found"
    shareList = []
    if (key == ""):
        key = "name"
    for student in students:
        try:
            shareList.append(
                {"id": student.get("id"), key : student.get(key)})
        except KeyError as e:
            return e
    return shareList


# -----------------------------------------------------------------------------------------------
# returns the courses roster into list
def getGroups(courseId, key='name'):
    groups = canvasCore.getGroups(courseId)
    if groups == "Error":
        return ("Course was Not Found")
    students = getDictofStudents(courseId, key)
    if groups == "Error":
        return ("Error Occured When Searching for Key")
    if (key == ""):
        key = "name"
    # students = {4221108: 'bkieffer04@gmail.com', 4221713: 'smmerz56@gmail.com'}
    # so I am not spamming their emails
    #students = {4221108: 'ajdeehring@gmail.com', 4221713: 'adam.deehring@gmail.com'}
    groupsJson = {}
    for group in groups:
        groupId = group.get('id')
        groupMembers = []
        members = canvasCore.getGroupMembers(groupId)
        for member in members:
            groupMembers.append(
                {"id": member.get("id"), key : students[member.get("id")]})
        groupsJson[group["name"]] = groupMembers
    return groupsJson

def getDictofStudents(courseId, key='name'):
    students = canvasCore.getCourseRoster(courseId)
    if students == "Error":
        return "Course was Not Found"
    shareList = {}
    if (key == ""):
        key = "name"
    for student in students:
        try:
            shareList[student.get("id")] = student.get(key)
        except KeyError as e:
            return "Error"
    return shareList


# -----------------------------------------------------------------------------------------------
# returns the courses roster into a csv file
def courseRoster():
    # force=True removes the content type requirement
    response = request.get_json(force=True)
    courseId = response.get('courseId')

    course = canvasCore.getCoursesName(courseId)

    if course != "Error":
        name = course.get('name')
        fileName = name + "-Roster.csv"

        writer = fileCreate(fileName)

        students = canvasCore.getCourseRoster(courseId)

        if students != "Error":

            for student in students:
                writer.writerow([student.get('name'), student.get('id')])

            return jsonify(message="Created CSV", status_code=200)
        else:
            return jsonify(message="Failed API call. Try again.", status_code=500)
    else:
        return jsonify(message="Failed. Course Doesnt Exist.", status_code=500)

# -----------------------------------------------------------------------------------------------
# Creates the file and writes the headers to the file
def fileCreate(fileName):
    path = str(Path.home() / "Downloads" / fileName)
    f = os.open(path, os.O_RDWR | os.O_CREAT, 0o666)
    fd = os.fdopen(f, "x", newline='')
    writer = csv.writer(fd)

    if "Groups" in fileName:
        writer.writerow(["studentName", "studentId",
                        "groupCategory", "groupName"])
    else:
        writer.writerow(["studentName", "studentId"])
    return writer
