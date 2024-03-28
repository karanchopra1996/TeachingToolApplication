import os, re, json
from flask import request, jsonify
from pathlib import Path

#This is called when importing settings and navigation from files
def fromFiles(courseID, settingsFile, navFile, canvasapi):
    """ Imports course and navigation (tabs) settings from files """


    if settingsFile is not None and navFile is not None:
        settings = json.load(settingsFile)
        if isinstance(settings, dict):#Makes sure the user added settings.json, which is in a dict
            status = canvasapi.course.update_settings(courseID, **settings)
            if status == 'Error':
                return 'Failed to import settings'
        else:
            return 'Settings file is in the incorrect format'
        
        nav = json.load(navFile)
        if isinstance(nav, list):#Makes sure the user added navigation.json, which is in a list
            status = importNavigation(nav, courseID, canvasapi)
            if status == 'Error':
                return 'Failed to import navigation'
        else:
            return 'Navigation file is in the incorrect format'

        return 'success'
    else:
        return 'Settings or Navigation file not set'

#-------------------------------------------------------------------------------
##This is called when exporting settings and navigation to json files
def toFile(course, settings, tabs):
   """ Exports course settings and navigation (tabs) to json files
   """
   settingsFileName = "{}-Settings.json".format(course.name)
   navFileName = "{}-Navigation.json".format(course.name)

   fileCreate(settings, settingsFileName)
   fileCreate(tabs, navFileName)
   
   return 'success'

#-----------------------------------------------------------------------------------------------
#Creates the settings and navigation json files
def fileCreate(settings, fileName):
    x = ""
    path = str(Path.home() / "Downloads" / fileName)
    f = os.open(path, os.O_RDWR|os.O_CREAT,0o666)
    fd = os.fdopen(f, "x", newline='')

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

#-------------------------------------------------------------------------------
def importNavigation(tabs, courseID, canvasapi):
    keys = ['label', 'position', 'hidden']
    for tab in tabs:
        tabID = tab.get('id')
        if tabID != 'home' and tabID != 'settings':
            kwargs = {key: tab.get(key) for key in keys}

            canvasapi.course.update_tab(courseID, tabID, **kwargs)
    return 'success'
