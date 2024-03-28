# from py import std
import requests, json, sys
from flask import request, jsonify
import csv
from core.canvas_services import canvas_services as canvasCore

#-----------------------------------------------------------------------------------------------
#ImportStudents
#Notes: 
    #In both groupInGroupCategory() and groupCategories() a while loop is needed because
        #if a group needs to be created, the request.get in each function needs to be called
        #again to get the updated group categories and groups to iterate over in both for loops.
        #This could be avoided if we were allowed to create a group/group category id.

#-----------------------------------------------------------------------------------------------
#Adds members to a specific group within a group category
def importManager():
    error = False
    courseId = request.form.get('courseId') 
    response = request.files.get('file')
    courseName = canvasCore.getCoursesName(courseId)
    
    if courseId != None and response != None and courseName != "Error": #courseName.get('name') != None:       
        csvfile  = response.stream.read().decode('utf-8').splitlines()
        input_file = csv.DictReader(csvfile)

        fieldnames = input_file.fieldnames

        if fieldnames[1] == "studentId" and fieldnames[2] == "groupCategory" and fieldnames[3] == "groupName":
            for row in input_file:

                studentId = row.get('studentId')
                groupCategoryName = row.get('groupCategory')
                groupName = row.get('groupName')

                groupCategoryId = startsWith(groupCategoryName)#This call and one below Redundant*************Why both
            
                #Enters if the user entered a group category name instead of an id number
                if isinstance(groupCategoryId, str):
                    groupCategoryId = groupCategories(courseId, groupCategoryName)#get specific group category in class
                
                groupId = groupInGroupCategory(groupCategoryId, groupName)#get specific group from group category
                response = canvasCore.updateGroup(groupId, studentId)
                
                if response == "Error":
                    error = True

            if error:
                return jsonify(message="Error: Some or all groups not created. Try again.",status_code=500)
            else:
                return jsonify(message="Groups created",status_code=200)
        else:
            return jsonify(message="Incorrect header naming",status_code=500)
    else:
        return jsonify(message="KeyError or Course Doesnt exist",status_code=500)
#-----------------------------------------------------------------------------------------------
#Checks to see if the user entered a number id instead of a name. Converts the number str to an int
def startsWith(entry):
    if(entry.startswith("0") or entry.startswith("1") or entry.startswith("2") or entry.startswith("3")
        or entry.startswith("4") or entry.startswith("5") or entry.startswith("6") or entry.startswith("7")
        or entry.startswith("8") or entry.startswith("9")):
        return int(entry)    

    return entry
#-----------------------------------------------------------------------------------------------
#Returns all the group categories from the course
#Precondition: the course id
def groupCategories(courseId, name):
    exists = False
    groupCategoryId = ""    
    
    while(exists == False):
        classGroupCategories = canvasCore.getGroupCategories(courseId)
        
        for groupCategory in classGroupCategories:
            if groupCategory.get('name') == name:
                groupCategoryId = groupCategory.get('id')
                exists = True
                break
        if exists == False:#if the group category listed on the csv is not in the course, create it
            response = canvasCore.createGroupCategory(courseId, name)
       
    return groupCategoryId
        
#-----------------------------------------------------------------------------------------------
#Returns the passed in group name's id from group category list.
#Precondition: The group category id 
def groupInGroupCategory(id, name):
    exists = False
    groupId = ""
    
    while(exists == False):
        groups = canvasCore.getGroupsInCategory(id)
        for group in groups:
            if group.get('name') == name:
                groupId = group.get('id')
                exists = True
                break
        if exists == False:#if the group listed on the csv is not in the course, create it
            response = canvasCore.createGroupInCategory(id, name)
    return groupId
    