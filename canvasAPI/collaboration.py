from .canvas_object import CanvasObject
from .paginated_list import PaginatedList
from .util import combine_kwargs
import csv

class Collaboration(CanvasObject):

    def get_collaborators(self, collaboration_id, **kwargs):
        return PaginatedList(
            self._requester,
            "GET",
            "collaborations/{}/members".format(collaboration_id),
            _root="collaborators",
            kwargs=combine_kwargs(**kwargs),
        )
    # ------------------------------------------------------------------------------
    ### Author: by Pooja Pal 
    # ------------------------------------------------------------------------------
    def exportToCSV(self, teams_info, assign_name):
        """
        Creates the CSV file and copies the contributors data from the comment section of the assignmnents
        :param teams_info: assignment collaborator details
        :type teams_info: List of dicts
        :param assign_name: Name of the assignment
        :type assign_name: string
        :rtype: Http Response object
        """
        fileName = assign_name + "_teams" + ".csv"
        try:
            with open(fileName, 'w') as csvFile:
                filewriter = csv.writer(csvFile, delimiter = ',')
                filewriter.writerow(['canvas_assignment_id','canvas_assignment_name', 'submission_id', 'submission_status','submitter_name','submitter_canvas_id', 'submitter_login_id','group_student_name','student_canvas_id','student_login_id','group_role',"Role" ])
                filewriter.writerow(['-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'])
                
                #teams_info contains team information from the submissions that are either submitted assignmnet ocontributors in the assignmnet
                #the nature of submission api response doesnt ensure all submitted assignmnets  to be listed before non submitted assignmnets 
                studentCanvasIds = []
                for team in teams_info:
                    if "membersData" in team:
                        for member in team['membersData']:
                            if member[1] not in studentCanvasIds:
                                filewriter.writerow([team['canvas_assignment_id'],assign_name,team['submission_id'],team['submission_status'],team['submitter_name'],team['submitter_canvas_id'],team['submitter_login_id'],member[0], member[1], member[2],member[3]]) 
                                studentCanvasIds.append(member[1]) 
                for team in teams_info:
                    if "membersData" not in team: 
                        if team['submitter_canvas_id'] not in studentCanvasIds:
                            filewriter.writerow([team['canvas_assignment_id'],assign_name,team['submission_id'],team['submission_status'],team['submitter_name'],team['submitter_canvas_id'],team['submitter_login_id'] ])
            return ("Successfully exported list of contributors ")   
        except Exception as ex:       
            return ("Error occured while exporting Contributor details for " + assign_name)   
    
        
        