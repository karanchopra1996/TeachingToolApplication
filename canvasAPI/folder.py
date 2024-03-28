from .canvas_object import CanvasObject
from .paginated_list import PaginatedList
from .upload import FileOrPathLike, Uploader
from .util import combine_kwargs


class Folder(CanvasObject):

   def copy_file(self, folder_id, file_id, **kwargs):
      """
      Copies a file into the current folder.

      :calls: `POST /api/v1/folders/:dest_folder_id/copy_file \
      <https://canvas.instructure.com/doc/api/files.html#method.folders.copy_file>`_

      :param file_id: The id of the source file.

      :rtype: dict
      """
      kwargs["source_file_id"] = file_id

      response = self._requester.request(
         "POST",
         "folders/{}/copy_file".format(folder_id),
         _kwargs=combine_kwargs(**kwargs),
      )
      return response.json()

   def create_folder(self, folder_id, name, **kwargs):
      """
      Creates a folder within this folder.

      :calls: `POST /api/v1/folders/:folder_id/folders \
      <https://canvas.instructure.com/doc/api/files.html#method.folders.create>`_

      :param name: The name of the folder.
      :type name: str
      :rtype: dict
      """
      response = self._requester.request(
         "POST",
         "folders/{}/folders".format(folder_id),
         name=name,
         _kwargs=combine_kwargs(**kwargs),
      )
      return response.json()

   def delete(self, folder_id, **kwargs):
      """
      Remove this folder. You can only delete empty folders unless you set the
         'force' flag.

      :calls: `DELETE /api/v1/folders/:id  \
      <https://canvas.instructure.com/doc/api/files.html#method.folders.api_destroy>`_

      :rtype: dict
      """
      response = self._requester.request(
         "DELETE", "folders/{}".format(folder_id), _kwargs=combine_kwargs(**kwargs)
      )
      return response.json()

   def get_files(self, folder_id, **kwargs):
      """
      Returns the paginated list of files for the folder.

      :calls: `GET /api/v1/folders/:id/files \
      <https://canvas.instructure.com/doc/api/files.html#method.files.api_index>`_

      :rtype: :class:`core.paginated_list.PaginatedList`
      """

      return PaginatedList(
         self._requester,
         "GET",
         "folders/{}/files".format(folder_id),
         _kwargs=combine_kwargs(**kwargs),
      )

   def get_folder(self, folder_id, **kwargs):
      """
      Return the details for a folder
      :calls: `GET /api/v1/folders/:id \
      <https://canvas.instructure.com/doc/api/files.html#method.folders.show>`_
      :rtype: dict
      """

      response = self._requester.request(
         "GET", "folders/{}".format(folder_id), _kwargs=combine_kwargs(**kwargs)
      )
      return response.json()

   def get_folders(self, folder_id, **kwargs):
      """
      Returns the paginated list of folders in the folder.

      :calls: `GET /api/v1/folders/:id/folders \
      <https://canvas.instructure.com/doc/api/files.html#method.folders.api_index>`_

      :rtype: :class:`core.paginated_list.PaginatedList`
      """
      return PaginatedList(
         self._requester, "GET", "folders/{}/folders".format(folder_id)
      )

   def update(self, folder_id, **kwargs):
      """
      Updates a folder.

      :calls: `PUT /api/v1/folders/:id \
      <https://canvas.instructure.com/doc/api/files.html#method.folders.update>`_

      :rtype: dict
      """
      response = self._requester.request(
         "PUT", "folders/{}".format(folder_id), _kwargs=combine_kwargs(**kwargs)
      )

      return response.json()

   def upload(self, folder_id, file: FileOrPathLike, **kwargs):
      """
      Upload a file to this folder.

      :calls: `POST /api/v1/folders/:folder_id/files \
      <https://canvas.instructure.com/doc/api/files.html#method.folders.create_file>`_

      :param file: The file or path of the file to upload.
      :type file: file or str
      :returns: True if the file uploaded successfully, False otherwise, \
                  and the JSON response from the API.
      :rtype: tuple
      """
      my_path = "folders/{}/files".format(folder_id)
      return Uploader(self._requester, my_path, file, **kwargs).start()