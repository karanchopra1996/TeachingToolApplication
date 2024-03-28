
import os
import io
from google.oauth2.credentials import Credentials
import requests

from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
from httplib2 import HttpLib2Error


class google_services():
    workspaceToFileConversions = {
        "application/vnd.google-apps.document":      ("application/vnd.openxmlformats-officedocument.wordprocessingml.document", ".docx"),
        "application/vnd.google-apps.presentation":  ("application/vnd.openxmlformats-officedocument.presentationml.presentation", ".pptx"),
        "application/vnd.google-apps.spreadsheet":   ("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", ".xlsx"),
    }
    SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/documents.readonly']
    DISCOVERY_DOC = 'https://docs.googleapis.com/$discovery/rest?version=v1'

    def get_credentials():
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth 2.0 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """

        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file(
                'token.json', google_services.SCOPES)
            # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', google_services.SCOPES)
                creds = flow.run_local_server(redirect_uri_trailing_slash=False)
                # Save the credentials for the next run
                with open('token.json', 'w') as token:
                    token.write(creds.to_json())
        return creds

    def createGoogleAccess():
        """
        Returns a Resource for interacting with the Drive v3 API.
        """
        creds = google_services.get_credentials()
        service = build('drive', 'v3', credentials=creds)
        return service
    
    # https://github.com/googleworkspace/python-samples/blob/main/drive/snippets/drive-v3/file_snippet/export_pdf.py
    def exportWorkspaceFile(real_file_id, file_type):
        """Download a Document file in PDF format.
        Args:
            real_file_id : file ID of any workspace document format file
        Returns : IO object with location
        """

        credentials = google_services.get_credentials()
        credentials.refresh(Request())

        try:
            # create drive api client
            service = build('drive', 'v3', credentials=credentials)

            file_id = real_file_id

            # pylint: disable=maybe-no-member
            request = service.files().export_media(fileId=file_id, mimeType=file_type)
            file = io.BytesIO()
            downloader = MediaIoBaseDownload(file, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()

        except HttpError as error:
            file = None

        return file.getvalue()

    # https://developers.google.com/drive/api/guides/manage-downloads
    def downloadDriveFile(real_file_id):
        """Downloads a file
        Args:
            real_file_id: ID of the file to download
        Returns : IO object with location.

        """
        credentials = google_services.get_credentials()
        credentials.refresh(Request())

        try:
            # create gmail api client
            service = build('drive', 'v3', credentials=credentials)

            file_id = real_file_id

            # pylint: disable=maybe-no-member
            request = service.files().get_media(fileId=file_id)
            file = io.BytesIO()
            downloader = MediaIoBaseDownload(file, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                #print(F'Download {int(status.progress() * 100)}.')
        except HttpError as error:
            # print(F'An error occurred: {error}')
            file = None

        return file.getvalue()

    # https://developers.google.com/drive/api/guides/folder
    def createDriveFolder(courseId, folderName, parentFolder):
        """ Create a folder and prints the folder ID
        Returns : Folder Id

        Load pre-authorized user credentials from the environment.
        TODO(developer) - See https://developers.google.com/identity
        for guides on implementing OAuth2 for the application.
        """
        credentials = google_services.get_credentials()
        credentials.refresh(Request())

        try:
            service = build('drive', 'v3', credentials=credentials)
            file_metadata = {
                'name': folderName,
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [parentFolder]

            }

            # pylint: disable=maybe-no-member
            file = service.files().create(body=file_metadata).execute()
            # print(F'Folder has created with ID: "{file.get("id")}".')

        except HttpError as error:
            # print(F'An error occurred: {error}')
            file = None

        return file

    # https://developers.google.com/drive/api/v2/reference/files/delete
    def deleteFile(file_id):
        credentials = google_services.get_credentials()
        credentials.refresh(Request())

        service = build('drive', 'v3', credentials=credentials)
        """Permanently delete a file, skipping the trash.

        Args:
            file_id: ID of the file to delete.
        """
        try:
            service.files().delete(fileId=file_id).execute()
            return ("Success")
        except HttpError as error:
            return ('An error occurred: ' + str(error))

    def uploadFileToGoogleDrive(fileName):
        googleAccess = google_services.createGoogleAccess()
        file_metadata = {'name': fileName,
                         'mimeType': 'application/vnd.google-apps.doc'}
        media = MediaFileUpload((fileName), mimetype='application/pdf')
        googleAccess.files().create(body=file_metadata,
                                    media_body=media, fields='id').execute()

    def getGoogleFiles():
        service = google_services.createGoogleAccess()

        resource = service.files()
        result = resource.list().execute()

        files = result.get('files')
        nextPageToken = result.get('nextPageToken')

        while nextPageToken:
            response = service.files().list(pageToken=nextPageToken).execute()
            files.extend(response.get('files'))
            nextPageToken = response.get('nextPageToken')
        return files

    def searchGoogleFiles(fileName):
        service = google_services.createGoogleAccess()
        itemNum = 0

        resource = service.files()
        result = resource.list().execute()

        files = result.get('files')
        nextPageToken = result.get('nextPageToken')

        while nextPageToken:
            response = service.files().list(pageToken=nextPageToken).execute()
            files.extend(response.get('files'))
            nextPageToken = response.get('nextPageToken')
            for itemNum in range(len(files)):
                if(files[itemNum]['name'] == fileName):
                    print("Found File")
                    return files[itemNum]
                itemNum += 1

    def determineFileType(driveFileType):
        return google_services.workspaceToFileConversions[driveFileType]

    # https://developers.google.com/drive/api/guides/manage-sharing#python
    def updateShares(real_file_id, real_user, access):
        """Batch permission modification.
        Args:
            real_file_id: file Id
            real_user: List of users
            real_domain: Domain of the user ID
        Prints modified permissions

        """
        credentials = google_services.get_credentials()
        credentials.refresh(Request())

        try:
            # create drive api client
            service = build('drive', 'v3', credentials=credentials)
            ids = []
            file_id = real_file_id

            def callback(request_id, response, exception):
                if exception:
                    ids.append((exception.reason, requests.codes.bad))
                else:
                    #print(f'Request_Id: {request_id}')
                    #print(F'Permission Id: {response.get("id")}')
                    ids.append(
                        (response.get('emailAddress'), requests.codes.ok))

                    # print(service.permissions().get(fileId=file_id,
                    #     permissionId=response.get('id')).to_json())

            # pylint: disable=maybe-no-member
            batch = service.new_batch_http_request(callback=callback)
            for user in real_user:
                user_permission = {
                    'type': 'user',
                    'role': access,
                    'emailAddress': user['email']
                }
                batch.add(service.permissions().create(fileId=file_id,
                                                       body=user_permission,
                                                       fields='id, emailAddress',))
            batch.execute()
            # print(service.permissions())

        except HttpError as error:
            ids = None
            return ('An error occurred: ' + error + '}', None)

        except HttpLib2Error as error:
            return ("Error occured when updating Permissions", None)

        erroredIDs = ''
        numOfSuc = 0
        for i in range(0, len(real_user)):
            if (ids[i][1] == 200):
                numOfSuc += 1
            else:
                erroredIDs += str(real_user[i]["id"]) + " "

        status = ""
        if (numOfSuc == len(real_user)):
            return "Success"
        else:
            status = "Error: " + \
                str(len(real_user) - numOfSuc) + \
                " email(s) failed, raised on Following ID(s): " + erroredIDs
        return status
