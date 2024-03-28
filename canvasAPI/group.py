from .canvas_object import CanvasObject
from .exceptions import RequiredFieldMissing
from .paginated_list import PaginatedList
from .upload import FileOrPathLike, Uploader
from .util import combine_kwargs, is_multivalued


class Group(CanvasObject):

   def get_group(self, group_id, **kwargs):
      """
      Return the data for a single group. If the caller does not
      have permission to view the group a 401 will be returned.
      :calls: `GET /api/v1/groups/:group_id \
      <https://canvas.instructure.com/doc/api/groups.html#method.groups.show>`_
      
      :rtype: dict
      """
      uri_str = "groups/{}"

      response = self._requester.request(
         "GET", uri_str.format(group_id), _kwargs=combine_kwargs(**kwargs)
      )
      return response.json()

   def get_group_category(self, category_id, **kwargs):
      """
      Get a single group category.
      :calls: `GET /api/v1/group_categories/:group_category_id \
      <https://canvas.instructure.com/doc/api/group_categories.html#method.group_categories.show>`_
      
      :rtype: dict
      """

      response = self._requester.request(
         "GET",
         "group_categories/{}".format(category_id),
         _kwargs=combine_kwargs(**kwargs),
      )
      return response.json()

   def create_discussion_topic(self, group_id, **kwargs):
      """
      Creates a new discussion topic for the course or group.

      :calls: `POST /api/v1/groups/:group_id/discussion_topics \
      <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics.create>`_

      :rtype: dict
      """
      response = self._requester.request(
         "POST",
         "groups/{}/discussion_topics".format(group_id),
         _kwargs=combine_kwargs(**kwargs),
      )

      response_json = response.json()
      response_json.update({"group_id": group_id})

      return response_json

   def create_folder(self, group_id, name, **kwargs):
      """
      Creates a folder in this group.

      :calls: `POST /api/v1/groups/:group_id/folders \
      <https://canvas.instructure.com/doc/api/files.html#method.folders.create>`_

      :param name: The name of the folder.
      :type name: str
      :rtype: dict
      """
      response = self._requester.request(
         "POST",
         "groups/{}/folders".format(group_id),
         name=name,
         _kwargs=combine_kwargs(**kwargs),
      )
      return response.json()

   def create_group(self, **kwargs):
      """
      Create a group
      :calls: `POST /api/v1/groups/ \
      <https://canvas.instructure.com/doc/api/groups.html#method.groups.create>`_
      :rtype: dict
      """
      response = self._requester.request(
         "POST", "groups", _kwargs=combine_kwargs(**kwargs)
      )
      return response.json()

   def create_membership(self, group_id, user_id, **kwargs):
      """
      Join, or request to join, a group, depending on the join_level of the group.
      If the membership or join request already exists, then it is simply returned.

      :calls: `POST /api/v1/groups/:group_id/memberships \
      <https://canvas.instructure.com/doc/api/groups.html#method.group_memberships.create>`_

      :rtype: dict
      """

      response = self._requester.request(
         "POST",
         "groups/{}/memberships".format(group_id),
         user_id=user_id,
         _kwargs=combine_kwargs(**kwargs),
      )
      return response.json()

   def create_page(self, group_id, wiki_page, **kwargs):
      """
      Create a new wiki page.

      :calls: `POST /api/v1/groups/:group_id/pages \
      <https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.create>`_

      :param wiki_page: Details about the page to create.
      :type wiki_page: dict
      :returns: The created page.
      :rtype: :class:`canvascore.page.Page`
      """

      if isinstance(wiki_page, dict) and "title" in wiki_page:
         kwargs["wiki_page"] = wiki_page
      else:
         raise RequiredFieldMissing("Dictionary with key 'title' is required.")

      response = self._requester.request(
         "POST", "groups/{}/pages".format(group_id), _kwargs=combine_kwargs(**kwargs)
      )

      page_json = response.json()
      page_json.update({"group_id": group_id})

      return page_json

   def delete(self, group_id, **kwargs):
      """
      Delete a group.

      :calls: `DELETE /api/v1/groups/:group_id \
      <https://canvas.instructure.com/doc/api/groups.html#method.groups.destroy>`_

      :rtype: dict
      """
      response = self._requester.request(
         "DELETE", "groups/{}".format(group_id), _kwargs=combine_kwargs(**kwargs)
      )
      return response.json()

   def edit(self, group_id, **kwargs):
      """
      Edit a group.

      :calls: `PUT /api/v1/groups/:group_id \
      <https://canvas.instructure.com/doc/api/groups.html#method.groups.update>`_

      :rtype: dict
      """
      response = self._requester.request(
         "PUT", "groups/{}".format(group_id), _kwargs=combine_kwargs(**kwargs)
      )
      return response.json()

   def edit_front_page(self, group_id, **kwargs):
      """
      Update the title or contents of the front page.

      :calls: `PUT /api/v1/groups/:group_id/front_page \
      <https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.update_front_page>`_

      :rtype: dict
      """

      response = self._requester.request(
         "PUT",
         "groups/{}/front_page".format(group_id),
         _kwargs=combine_kwargs(**kwargs),
      )
      page_json = response.json()
      page_json.update({"group_id": group_id})

      return page_json

   def export_content(self, group_id, export_type, **kwargs):
      """
      Begin a content export job for a group.

      :calls: `POST /api/v1/groups/:group_id/content_exports\
      <https://canvas.instructure.com/doc/api/content_exports.html#method.content_exports_api.create>`_

      :param export_type: The type of content to export.
      :type export_type: str

      :rtype: dict
      """

      kwargs["export_type"] = export_type

      response = self._requester.request(
         "POST",
         "groups/{}/content_exports".format(group_id),
         _kwargs=combine_kwargs(**kwargs),
      )
      return response.json()

   def get_activity_stream_summary(self, group_id, **kwargs):
      """
      Return a summary of the current user's global activity stream.

      :calls: `GET /api/v1/groups/:group_id/activity_stream/summary \
      <https://canvas.instructure.com/doc/api/groups.html#method.groups.activity_stream_summary>`_

      :rtype: dict
      """
      response = self._requester.request(
         "GET",
         "groups/{}/activity_stream/summary".format(group_id),
         _kwargs=combine_kwargs(**kwargs),
      )
      return response.json()

   def get_assignment_override(self, group_id, assignment_id, **kwargs):
      """
      Return override for the specified assignment for this group.

      :calls: `GET /api/v1/groups/:group_id/assignments/:assignment_id/override \
      <https://canvas.instructure.com/doc/api/assignments.html#method.assignment_overrides.group_alias>`_

      :rtype: dict
      """

      response = self._requester.request(
         "GET", "groups/{}/assignments/{}/override".format(group_id, assignment_id)
      )
      return response.json()

   def get_collaborations(self, group_id, **kwargs):
      """
      Return a list of collaborations for a given group ID.

      :calls: `GET /api/v1/groups/:group_id/collaborations \
      <https://canvas.instructure.com/doc/api/collaborations.html#method.collaborations.api_index>`_

      :rtype: :class: 'canvasAPI.paginated_list.PaginatedList'
      """
      return PaginatedList(
         self._requester,
         "GET",
         "groups/{}/collaborations".format(group_id),
         _root="collaborations",
         kwargs=combine_kwargs(**kwargs),
      )

   def get_potential_collaborators(self, group_id, **kwargs):
      """
      Returns a paginated list of the users who can potentially be added to a 
      collaboration in the group.

      :calls: `GET /api/v1/courses/:course_id/potential_collaborators
      <https://canvas.instructure.com/doc/api/collaborations.html#method.collaborations.potential_collaborators>`_
      :rtype: :class:`canvasAPI.paginated_list.PaginatedList`
      """ 
      return PaginatedList(
         self._requester,
         "GET",
         "groups/{}/potential_collaborators".format(group_id),
         _kwargs=combine_kwargs(**kwargs),
      )

   def get_content_export(self, group_id, export_id, **kwargs):
      """
      Return information about a single content export.

      :calls: `GET /api/v1/groups/:group_id/content_exports/:id\
      <https://canvas.instructure.com/doc/api/content_exports.html#method.content_exports_api.show>`_

      :rtype: dict
      """

      response = self._requester.request(
         "GET",
         "groups/{}/content_exports/{}".format(group_id, export_id),
         _kwargs=combine_kwargs(**kwargs),
      )

      return response.json()

   def get_content_exports(self, group_id, **kwargs):
      """
      Return a paginated list of the past and pending content export jobs for a group.

      :calls: `GET /api/v1/groups/:group_id/content_exports\
      <https://canvas.instructure.com/doc/api/content_exports.html#method.content_exports_api.index>`_

      :rtype: :class:`canvascore.paginated_list.PaginatedList`
      """

      return PaginatedList(
         self._requester,
         "GET",
         "groups/{}/content_exports".format(group_id),
         kwargs=combine_kwargs(**kwargs),
      )

   def get_discussion_topic(self, group_id, topic_id, **kwargs):
      """
      Return data on an individual discussion topic.

      :calls: `GET /api/v1/groups/:group_id/discussion_topics/:topic_id \
      <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics_api.show>`_

      :rtype: dict
      """

      response = self._requester.request(
         "GET",
         "groups/{}/discussion_topics/{}".format(group_id, topic_id),
         _kwargs=combine_kwargs(**kwargs),
      )

      response_json = response.json()
      response_json.update({"group_id": group_id})

      return response_json

   def get_discussion_topics(self, group_id, **kwargs):
      """
      Returns the paginated list of discussion topics for this course or group.

      :calls: `GET /api/v1/groups/:group_id/discussion_topics \
      <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics.index>`_

      :rtype: :class:`canvascore.paginated_list.PaginatedList`
      """

      return PaginatedList(
         self._requester,
         "GET",
         "groups/{}/discussion_topics".format(group_id),
         {"group_id": group_id},
         _kwargs=combine_kwargs(**kwargs),
      )

   def get_external_feeds(self, group_id, **kwargs):
      """
      Returns the list of External Feeds this group.

      :calls: `GET /api/v1/groups/:group_id/external_feeds \
      <https://canvas.instructure.com/doc/api/announcement_external_feeds.html#method.external_feeds.index>`_

      :rtype: :class:`canvascore.paginated_list.PaginatedList`
      """

      return PaginatedList(
         self._requester,
         "GET",
         "groups/{}/external_feeds".format(group_id),
      )

   def get_file(self, group_id, file_id, **kwargs):
      """
      Return the standard attachment json object for a file.

      :calls: `GET /api/v1/groups/:group_id/files/:id \
      <https://canvas.instructure.com/doc/api/files.html#method.files.api_show>`_

      :param file: The object or ID of the file to retrieve.
      :type file: :class:`canvascore.file.File` or int

      :rtype: :class:`canvascore.file.File`
      """

      response = self._requester.request(
         "GET",
         "groups/{}/files/{}".format(group_id, file_id),
         _kwargs=combine_kwargs(**kwargs),
      )
      return response.json()

   def get_file_quota(self, group_id, **kwargs):
      """
      Returns the total and used storage quota for the group.

      :calls: `GET /api/v1/groups/:group_id/files/quota \
      <https://canvas.instructure.com/doc/api/files.html#method.files.api_quota>`_

      :rtype: dict
      """

      response = self._requester.request(
         "GET",
         "groups/{}/files/quota".format(group_id),
         _kwargs=combine_kwargs(**kwargs),
      )

      return response.json()

   def get_files(self, group_id, **kwargs):
      """
      Returns the paginated list of files for the group.

      :calls: `GET /api/v1/groups/:group_id/files \
      <https://canvas.instructure.com/doc/api/files.html#method.files.api_index>`_

      :rtype: :class:`canvascore.paginated_list.PaginatedList`
      """

      return PaginatedList(
         self._requester,
         "GET",
         "groups/{}/files".format(group_id),
         _kwargs=combine_kwargs(**kwargs),
      )

   def get_folder(self, group_id, folder_id, **kwargs):
      """
      Returns the details for a group's folder

      :calls: `GET /api/v1/groups/:group_id/folders/:id \
      <https://canvas.instructure.com/doc/api/files.html#method.folders.show>`_

      :param folder: The object or ID of the folder to retrieve.
      :type folder: :class:`canvascore.folder.Folder` or int

      :rtype: dict
      """

      response = self._requester.request(
         "GET",
         "groups/{}/folders/{}".format(group_id, folder_id),
         _kwargs=combine_kwargs(**kwargs),
      )
      return response.json()

   def get_folders(self, group_id, **kwargs):
      """
      Returns the paginated list of all folders for the given group. This will be returned as a
      flat list containing all subfolders as well.

      :calls: `GET /api/v1/groups/:group_id/folders \
      <https://canvas.instructure.com/doc/api/files.html#method.folders.list_all_folders>`_

      :rtype: :class:`canvascore.paginated_list.PaginatedList`
      """
      return PaginatedList(
         self._requester, "GET", "groups/{}/folders".format(group_id)
      )


   def get_membership(self, group_id, user_id, membership_type, **kwargs):
      """
      List users in a group.

      :calls: `GET /api/v1/groups/:group_id/users/:user_id \
         <https://canvas.instructure.com/doc/api/groups.html#method.group_memberships.show>`_

         or `GET /api/v1/groups/:group_id/memberships/:membership_id
         <https://canvas.instructure.com/doc/api/groups.html#method.group_memberships.show>`_

      :param user_id: user ID or membership ID
      :param membership_type: 'users' or 'memberships'

      :rtype: dict
      """

      response = self._requester.request(
         "GET",
         "groups/{}/{}/{}".format(group_id, membership_type, user_id),
         _kwargs=combine_kwargs(**kwargs),
      )
      return response.json()

   def get_memberships(self, group_id, **kwargs):
      """
      List users in a group.

      :calls: `GET /api/v1/groups/:group_id/memberships \
      <https://canvas.instructure.com/doc/api/groups.html#method.group_memberships.index>`_

      :rtype: :class:`canvascore.paginated_list.PaginatedList`
      """
      return PaginatedList(
         self._requester,
         "GET",
         "groups/{}/memberships".format(group_id),
         _kwargs=combine_kwargs(**kwargs),
      )

   def get_page(self, group_id, page_url, **kwargs):
      """
      Retrieve the contents of a wiki page.

      :calls: `GET /api/v1/groups/:group_id/pages/:url \
      <https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.show>`_

      :param url: The url for the page.
      :type url: str
      :returns: The specified page.
      :rtype: dict
      """

      response = self._requester.request(
         "GET",
         "groups/{}/pages/{}".format(group_id, page_url),
         _kwargs=combine_kwargs(**kwargs),
      )
      page_json = response.json()
      page_json.update({"group_id": group_id})

      return page_json

   def get_pages(self, group_id, **kwargs):
      """
      List the wiki pages associated with a group.

      :calls: `GET /api/v1/groups/:group_id/pages \
      <https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.index>`_

      :rtype: :class:`canvascore.paginated_list.PaginatedList`
      """

      return PaginatedList(
         self._requester,
         "GET",
         "groups/{}/pages".format(group_id),
         {"group_id": group_id},
         _kwargs=combine_kwargs(**kwargs),
      )

   def get_tabs(self, group_id, **kwargs):
      """
      List available tabs for a group.
      Returns a list of navigation tabs available in the current context.

      :calls: `GET /api/v1/groups/:group_id/tabs \
      <https://canvas.instructure.com/doc/api/tabs.html#method.tabs.index>`_

      :rtype: :class:`canvascore.paginated_list.PaginatedList`
      """

      return PaginatedList(
         self._requester,
         "GET",
         "groups/{}/tabs".format(group_id),
         {"group_id": group_id},
         _kwargs=combine_kwargs(**kwargs),
      )

   def get_users(self, group_id, **kwargs):
      """
      List users in a group.

      :calls: `GET /api/v1/groups/:group_id/users \
      <https://canvas.instructure.com/doc/api/groups.html#method.groups.users>`_

      :rtype: :class:`canvascore.paginated_list.PaginatedList`
      """

      return PaginatedList(
         self._requester,
         "GET",
         "groups/{}/users".format(group_id),
         _kwargs=combine_kwargs(**kwargs),
      )

   def invite(self, group_id, invitees, **kwargs):
      """
      Invite users to group.

      :calls: `POST /api/v1/groups/:group_id/invite \
      <https://canvas.instructure.com/doc/api/groups.html#method.groups.invite>`_

      :param invitees: list of user ids
      :type invitees: integer list

      :rtype: :class:`canvascore.paginated_list.PaginatedList`
      """
      kwargs["invitees"] = invitees
      
      return PaginatedList(
         self._requester,
         "POST",
         "groups/{}/invite".format(group_id),
         _kwargs=combine_kwargs(**kwargs),
      )

   def preview_html(self, group_id, html, **kwargs):
      """
      Preview HTML content processed for this course.

      :calls: `POST /api/v1/groups/:group_id/preview_html \
      <https://canvas.instructure.com/doc/api/groups.html#method.groups.preview_html>`_

      :param html: The HTML code to preview.
      :type html: str
      :rtype: str
      """
      response = self._requester.request(
         "POST",
         "groups/{}/preview_html".format(group_id),
         html=html,
         _kwargs=combine_kwargs(**kwargs),
      )
      return response.json().get("html", "")


   def remove_user(self, group_id, user_id, **kwargs):
      """
      Leave a group if allowed.

      :calls: `DELETE /api/v1/groups/:group_id/users/:user_id \
      <https://canvas.instructure.com/doc/api/groups.html#method.group_memberships.destroy>`_


      :rtype: dict
      """

      response = self._requester.request(
         "DELETE",
         "groups/{}/users/{}".format(group_id, user_id),
         _kwargs=combine_kwargs(**kwargs),
      )
      return response.json()

   def reorder_pinned_topics(self, group_id, order, **kwargs):
      """
      Puts the pinned discussion topics in the specified order.
      All pinned topics should be included.

      :calls: `POST /api/v1/groups/:group_id/discussion_topics/reorder \
      <https://canvas.instructure.com/doc/api/discussion_topics.html#method.discussion_topics.reorder>`_

      :param order: The ids of the pinned discussion topics in the desired order.
         e.g. [104, 102, 103]
      :type order: iterable sequence of values

      :rtype: :class:`canvascore.paginated_list.PaginatedList`
      """
      # Convert list or tuple to comma-separated string
      if is_multivalued(order):
         order = ",".join([str(topic_id) for topic_id in order])

      # Check if is a string with commas
      if not isinstance(order, str) or "," not in order:
         raise ValueError("Param `order` must be a list, tuple, or string.")

      kwargs["order"] = order

      response = self._requester.request(
         "POST",
         "groups/{}/discussion_topics/reorder".format(group_id),
         _kwargs=combine_kwargs(**kwargs),
      )

      return response.json().get("reorder")

   def resolve_path(self, group_id, full_path=None, **kwargs):
      """
      Returns the paginated list of all of the folders in the given
      path starting at the group root folder. Returns root folder if called
      with no arguments.

      :calls: `GET /api/v1/groups/group_id/folders/by_path/*full_path \
      <https://canvas.instructure.com/doc/api/files.html#method.folders.resolve_path>`_

      :param full_path: Full path to resolve, relative to group root.
      :type full_path: string

      :rtype: :class:`canvascore.paginated_list.PaginatedList`
      """

      if full_path:
         return PaginatedList(
               self._requester,
               "GET",
               "groups/{0}/folders/by_path/{1}".format(group_id, full_path),
               _kwargs=combine_kwargs(**kwargs),
         )
      else:
         return PaginatedList(
               self._requester,
               "GET",
               "groups/{0}/folders/by_path".format(group_id),
               _kwargs=combine_kwargs(**kwargs),
         )

   def show_front_page(self, group_id, **kwargs):
      """
      Retrieve the content of the front page.

      :calls: `GET /api/v1/groups/:group_id/front_page \
      <https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.show_front_page>`_

      :rtype: dict
      """
      response = self._requester.request(
         "GET",
         "groups/{}/front_page".format(group_id),
         _kwargs=combine_kwargs(**kwargs),
      )
      page_json = response.json()
      page_json.update({"group_id": group_id})

      return page_json

   def update_membership(self, group_id, user_id, **kwargs):
      """
      Accept a membership request, or add/remove moderator rights.

      :calls: `PUT /api/v1/groups/:group_id/users/:user_id \
      <https://canvas.instructure.com/doc/api/groups.html#method.group_memberships.update>`_

      :rtype: dict
      """

      response = self._requester.request(
         "PUT",
         "groups/{}/users/{}".format(group_id, user_id),
         _kwargs=combine_kwargs(**kwargs),
      )
      return response.json()

   def upload(self, group_id, file: FileOrPathLike, **kwargs):
      """
      Upload a file to the group.
      Only those with the 'Manage Files' permission on a group can upload files to the group.
      By default, this is anybody participating in the group, or any admin over the group.

      :calls: `POST /api/v1/groups/:group_id/files \
      <https://canvas.instructure.com/doc/api/groups.html#method.groups.create_file>`_

      :param path: The path of the file to upload.
      :type path: str
      :param file: The file or path of the file to upload.
      :type file: file or str
      :returns: True if the file uploaded successfully, False otherwise, \
                  and the JSON response from the API.
      :rtype: tuple
      """

      return Uploader(
         self._requester, "groups/{}/files".format(group_id), file, **kwargs
      ).start()

   def remove_membership_self(self, membership_id, **kwargs):
      """
      Leave a group if allowed.

      :calls: `DELETE /api/v1/groups/:group_id/memberships/:membership_id \
      <https://canvas.instructure.com/doc/api/groups.html#method.group_memberships.destroy>`_

      :returns: An empty dictionary
      :rtype: dict
      """
      response = self._requester.request(
         "DELETE",
         "groups/{}/memberships/self".format(membership_id),
         _kwargs=combine_kwargs(**kwargs),
      )
      return response.json()

   def remove_membership_user(self, membership_id, user_id, **kwargs):
      """
      Remove user from membership.

      :calls: `DELETE /api/v1/groups/:group_id/users/:user_id \
      <https://canvas.instructure.com/doc/api/groups.html#method.group_memberships.destroy>`_

      :returns: An empty dictionary
      :rtype: dict
      """

      response = self._requester.request(
         "DELETE",
         "groups/{}/users/{}".format(membership_id, user_id),
         _kwargs=combine_kwargs(**kwargs),
      )
      return response.json()

   def update_membership(self, group_id, membership_id, **kwargs):
      """
      Accept a membership request, or add/remove moderator rights.

      :calls: `PUT /api/v1/groups/:group_id/memberships/:membership_id \
      <https://canvas.instructure.com/doc/api/groups.html#method.group_memberships.update>`_

      :rtype: dict
      """

      response = self._requester.request(
         "PUT",
         "groups/{}/memberships/{}".format(group_id, membership_id),
         _kwargs=combine_kwargs(**kwargs),
      )
      return response.json()

   def assign_members_to_category(self, group_category_id, **kwargs):
      """
      Assign unassigned members.

      :calls: `POST /api/v1/group_categories/:group_category_id/assign_unassigned_members \
      <https://canvas.instructure.com/doc/api/group_categories.html#method.group_categories.assign_unassigned_members>`_

      :rtype: :class:`canvascore.paginated_list.PaginatedList`
      """

      response = self._requester.request(
         "POST",
         "group_categories/{}/assign_unassigned_members".format(group_category_id),
         _kwargs=combine_kwargs(**kwargs),
      )
      return response.json()

   def create_group_in_category(self, group_category_id, **kwargs):
      """
      Create a group.

      :calls: `POST /api/v1/group_categories/:group_category_id/groups \
      <https://canvas.instructure.com/doc/api/groups.html#method.groups.create>`_

      :rtype: dict
      """
      response = self._requester.request(
         "POST",
         "group_categories/{}/groups".format(group_category_id),
         _kwargs=combine_kwargs(**kwargs),
      )
      return response.json()

   def delete_group_category(self, group_category_id, **kwargs):
      """
      Delete a group category.

      :calls: `DELETE /api/v1/group_categories/:group_category_id \
      <https://canvas.instructure.com/doc/api/group_categories.html#method.group_categories.destroy>`_

      :rtype: empty dict
      """
      response = self._requester.request(
         "DELETE",
         "group_categories/{}".format(group_category_id),
         _kwargs=combine_kwargs(**kwargs),
      )
      return response.json()

   def get_groups_in_category(self, group_category_id, **kwargs):
      """
      List groups in group category.

      :calls: `GET /api/v1/group_categories/:group_category_id/groups \
      <https://canvas.instructure.com/doc/api/group_categories.html#method.group_categories.groups>`_

      :rtype: :class:`canvascore.paginated_list.PaginatedList`
      """
      return PaginatedList(
         self._requester, "GET", "group_categories/{}/groups".format(group_category_id)
      )

   def get_users_in_category(self, group_category_id, **kwargs):
      """
      List users in group category.

      :calls: `GET /api/v1/group_categories/:group_category_id/users \
      <https://canvas.instructure.com/doc/api/group_categories.html#method.group_categories.users>`_

      :rtype: :class:`canvascore.paginated_list.PaginatedList` 
      """

      return PaginatedList(
         self._requester,
         "GET",
         "group_categories/{}/users".format(group_category_id),
         _kwargs=combine_kwargs(**kwargs),
      )

   def update_group_category(self, group_category_id, **kwargs):
      """
      Update a group category.

      :calls: `PUT /api/v1/group_categories/:group_category_id \
      <https://canvas.instructure.com/doc/api/group_categories.html#method.group_categories.update>`_

      :rtype: dict
      """
      response = self._requester.request(
         "PUT",
         "group_categories/{}".format(group_category_id),
         _kwargs=combine_kwargs(**kwargs),
      )
      return response.json()
   
   def import_category_groups(self, group_category_id, **kwargs):
      """
      Create Groups in a Group Category through a CSV import
      :calls: `POST /api/v1/group_categories/:group_category_id/import \
      <https://canvas.instructure.com/doc/api/group_categories.html#method.group_categories.import>`_

      Group category csv format requirements: 
      <https://canvas.instructure.com/doc/api/file.group_category_csv.html>
      """
      response = self._requester.request(
         "POST",
         "group_categories/{}/import".format(group_category_id),
         _kwargs=combine_kwargs(**kwargs),
      )
      return response.json()