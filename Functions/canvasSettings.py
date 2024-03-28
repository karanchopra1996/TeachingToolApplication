import json, os
import re
from flask import request, jsonify
from pathlib import Path
from core.canvas_services import canvas_services as canvasCore

#-----------------------------------------------------------------------------------------------
#This is called when importing settings and navigation directly from another course favorite
def settingsManager():
    response = request.get_json(force=True)
    exportCourse = response.get('courseId')
    importCourse = response.get('importCourse')

    settings = canvasCore.getSettings(exportCourse)
    tabs = canvasCore.getNavigation(exportCourse)
    
    if settings != "Error" and tabs != "Error":
        status = importSettings(importCourse, settings)
        
        if status == 'Failed':
            return jsonify(message="Failed to Import Settings. Importing navigation was not attempted.", status_code=500)
        else:
            return importNavigation(importCourse, tabs)
    else:
        return jsonify(message="Failed to Import Settings and Navigation.", status_code=500)
    
#-----------------------------------------------------------------------------------------------
#This is called when importing settings and navigation from files
def fromFiles():
    settingsFail = False
    navFail = False
    courseId = request.form.get('courseId')
    settingsFile = request.files.get('settingsFile')
    navFile = request.files.get('navFile')


    if courseId != None and settingsFile != None and navFile != None and canvasCore.getCoursesName(courseId) != "Error":
        settings = json.load(settingsFile)
        if isinstance(settings, dict):#Makes sure the user added settings.json, which is in a dict
            status = importSettings(courseId, settings)
            if status == 'Failed':
                settingsFail = True
        else:
            settingsFail = True
        
        nav = json.load(navFile)
        if isinstance(nav, list):#Makes sure the user added navigation.json, which is in a list
            status = importNavigation(courseId, nav)
            if status == 'Failed':
                navFail = True
        else:
            navFail = True

        if settingsFail == True or navFail == True:
            return jsonify(message="Failed to import settings or navigation", status_code=500)
        
        return jsonify(message="Imported settings and navigation to course.", status_code=200)
    else:
        return jsonify(message="KeyError or Course Doesnt exist", status_code=500)
#-----------------------------------------------------------------------------------------------
##This is called when exporting settings and navigation to json files
def toFile():
    
    response = request.get_json(force=True)
    exportCourse = response.get('courseId')

    if exportCourse != None:
        fileName = "-Settings.json"
        fileName = createFileName(exportCourse, fileName)
        settings = canvasCore.getSettings(exportCourse)

        fileName2 = "-Navigation.json"
        navFileName = createFileName(exportCourse, fileName2)
        navigation = canvasCore.getNavigation(exportCourse)

        if fileName != "Fail" and settings != "Error" and navFileName != "Error" and navigation != "Error":

            fileCreate(settings, fileName)
           
            fileCreate(navigation, navFileName)
        
            return jsonify(message="Course Settings and Navigation exported to files", status_code=200)
        else:
            return jsonify(message="Failed API call or failed to create file. Try again.", status_code=500) 
    else:
        return jsonify(message="Failed. Course doesn't exist.", status_code=500)
#-----------------------------------------------------------------------------------------------
#Creates file name
def createFileName(courseId, fileName):
    course = canvasCore.getCoursesName(courseId)
    
    if course != "Error":
        name = course.get('name')
        fileName = name + fileName
    else:
        fileName = "Fail"

    return fileName

#-----------------------------------------------------------------------------------------------
#Creates the settings and navigation json files
def fileCreate(settings, fileName):
    x = ""
    path = str(Path.home() / "Downloads" / fileName)
    f = os.open(path, os.O_RDWR|os.O_CREAT,0o666)
    fd = os.fdopen(f, "x",newline='')

    if "Settings" in fileName:
        x = modifyJson(settings)
    else:
        x = modifyNavigation(settings)    
    
    fd.write(x)

#-----------------------------------------------------------------------------------------------
#Modifies the Navigation Json file so it is more readable
def modifyNavigation(settings):
    parameters = "["
    i = 0
    for tab in settings:
        if tab.get('hidden') == None or tab.get('hidden') == "False":
            parameters = parameters + "{\"label\":\""+tab.get("label")+"\",\"position\":\""+str(tab.get("position"))+"\",\"hidden\":\"False\""+",\"id\":\""+tab.get("id")+"\"}"
        else:
            parameters = parameters + "{\"label\":\""+tab.get("label")+"\",\"position\":\""+str(tab.get("position"))+"\",\"hidden\":\"True\""+",\"id\":\""+tab.get("id")+"\"}"
        if i != len(settings)-1:
            parameters += ","
        parameters += "\r\n"
        i += 1
    parameters += "]"
    x = str(parameters).replace("'",'"')
    return x

#-----------------------------------------------------------------------------------------------
#Modifies the settings Json file to be more readable and so it is understood by Canvas
def modifyJson(settings):

    string = str(settings).replace("'",'"')
    string = str(string).replace(",",",\r\n")

    string = re.sub(r': (?!")',': "', string)
    string = re.sub(r'(?<=\w),\r\n','",\r\n', string)
    string = re.sub(r'(?<=\w)\}','"}', string)

    return string

#-----------------------------------------------------------------------------------------------
#Takes the settings exported from a course and applies them to a new course
def importSettings(courseId, settings):
    parameters = ""
    
    i = 0
    for key,value in settings.items():
        parameters += key + "=" + str(value)
        if i < len(settings.items()) - 1:
            parameters += "&"
        i += 1
    
    #response = canvasCore.updateSettings(courseId, parameters)
    response = canvasCore.updateSettings(courseId, settings)
    
    if response == "Error":
        return "Failed"
        
    return "Canvas Settings Applied"
    
#-----------------------------------------------------------------------------------------------
#Takes the navigation(tabs) exported from a course and applies them to a new course
def importNavigation(importCourse, tabs):
    
    failed = False
    for tab in tabs:
        
        parameters = ""
        if tab.get("id") != 'home' and tab.get("id") != 'settings':
            
            if (tab.get('hidden') == None) or (tab.get('hidden') == "False"):      
                parameters = "position="+str(tab.get('position')) + "&hidden=False"
            else:
                parameters = "hidden=True"
                
            response = canvasCore.updateNavigation(importCourse, str(tab.get("id")), parameters)
            
            if response == "Error":
                failed = True
    if failed:
        return "Failed"

    return jsonify(message="Course Settings and Navigation imported", status_code=200)