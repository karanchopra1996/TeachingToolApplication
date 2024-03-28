from .canvas_object import CanvasObject
from .exceptions import RequiredFieldMissing
from .paginated_list import PaginatedList
from .util import combine_kwargs


class Module(CanvasObject):

   def create_module_item(self, course_id, module_id, module_item, **kwargs):
      """
      Create a module item.

      :calls: `POST /api/v1/courses/:course_id/modules/:module_id/items \
      <https://canvas.instructure.com/doc/api/modules.html#method.context_module_items_api.create>`_

      :param module_item: The attributes to create the module item with.
      :type module_item: dict
      :returns: The created module item.
      :rtype: dict
      """

      unrequired_types = ["ExternalUrl", "Page", "SubHeader"]

      if isinstance(module_item, dict) and "type" in module_item:
         # content_id is not required for unrequired_types
         if module_item["type"] in unrequired_types or "content_id" in module_item:
               kwargs["module_item"] = module_item
         else:
               raise RequiredFieldMissing(
                  "Dictionary with key 'content_id' is required."
               )
      else:
         raise RequiredFieldMissing("Dictionary with key 'type' is required.")

      response = self._requester.request(
         "POST",
         "courses/{}/modules/{}/items".format(course_id, module_id),
         _kwargs=combine_kwargs(**kwargs),
      )
      module_item_json = response.json()
      module_item_json.update({"course_id": course_id})

      return module_item_json

   def delete(self, course_id, module_id, **kwargs):
      """
      Delete this module.

      :calls: `DELETE /api/v1/courses/:course_id/modules/:id \
      <https://canvas.instructure.com/doc/api/modules.html#method.context_modules_api.destroy>`_

      :rtype: dict
      """
      response = self._requester.request(
         "DELETE",
         "courses/{}/modules/{}".format(course_id, module_id),
         _kwargs=combine_kwargs(**kwargs),
      )
      module_json = response.json()
      module_json.update({"course_id": course_id})

      return module_json

   def edit(self, course_id, module_id, **kwargs):
      """
      Update this module.

      :calls: `PUT /api/v1/courses/:course_id/modules/:id \
      <https://canvas.instructure.com/doc/api/modules.html#method.context_modules_api.update>`_

      :rtype: dict
      """
      response = self._requester.request(
         "PUT",
         "courses/{}/modules/{}".format(course_id, module_id),
         _kwargs=combine_kwargs(**kwargs),
      )
      module_json = response.json()
      module_json.update({"course_id": course_id})

      return module_json

   def get_module_item(self, course_id, module_id, module_item_id, **kwargs):
      """
      Retrieve a module item by ID.

      :calls: `GET /api/v1/courses/:course_id/modules/:module_id/items/:id \
      <https://canvas.instructure.com/doc/api/modules.html#method.context_module_items_api.show>`_

      :rtype: dict
      """

      response = self._requester.request(
         "GET",
         "courses/{}/modules/{}/items/{}".format(
               course_id, module_id, module_item_id
         ),
         _kwargs=combine_kwargs(**kwargs),
      )
      module_item_json = response.json()
      module_item_json.update({"course_id": course_id})

      return module_item_json

   def get_module_items(self, course_id, module_id, **kwargs):
      """
      List all of the items in this module.

      :calls: `GET /api/v1/courses/:course_id/modules/:module_id/items \
      <https://canvas.instructure.com/doc/api/modules.html#method.context_module_items_api.index>`_

      :rtype: :class:`canvasAPI.paginated_list.PaginatedList`
      """
      return PaginatedList(
         self._requester,
         "GET",
         "courses/{}/modules/{}/items".format(course_id, module_id),
         {"course_id": course_id},
         _kwargs=combine_kwargs(**kwargs),
      )

   def relock(self, course_id, module_id, **kwargs):
      """
      Reset module progressions to their default locked state and recalculates
      them based on the current requirements.

      Adding progression requirements to an active course will not lock students
      out of modules they have already unlocked unless this action is called.

      :calls: `PUT /api/v1/courses/:course_id/modules/:id/relock \
      <https://canvas.instructure.com/doc/api/modules.html#method.context_modules_api.relock>`_

      :rtype: dict
      """
      response = self._requester.request(
         "PUT",
         "courses/{}/modules/{}/relock".format(course_id, module_id),
         _kwargs=combine_kwargs(**kwargs),
      )
      module_json = response.json()
      module_json.update({"course_id": course_id})

      return module_json

   def complete_module_item(self, course_id, module_id, module_item_id, **kwargs):
      """
      Mark this module item as done.

      :calls: `PUT /api/v1/courses/:course_id/modules/:module_id/items/:id/done \
      <https://canvas.instructure.com/doc/api/modules.html#method.context_module_items_api.mark_as_done>`_

      :rtype: dict
      """
      response = self._requester.request(
         "PUT",
         "courses/{}/modules/{}/items/{}/done".format(
               course_id, module_id, module_item_id
         ),
         _kwargs=combine_kwargs(**kwargs),
      )
      module_item_json = response.json()
      module_item_json.update({"course_id": course_id})

      return module_item_json

   def delete_module_item(self, course_id, module_id, module_item_id, **kwargs):
      """
      Delete this module item.

      :calls: `DELETE /api/v1/courses/:course_id/modules/:module_id/items/:id \
      <https://canvas.instructure.com/doc/api/modules.html#method.context_module_items_api.destroy>`_

      :rtype: dict
      """
      response = self._requester.request(
         "DELETE",
         "courses/{}/modules/{}/items/{}".format(
               course_id, module_id, module_item_id
         ),
         _kwargs=combine_kwargs(**kwargs),
      )
      module_item_json = response.json()
      module_item_json.update({"course_id": course_id})

      return module_item_json

   def edit_module_item(self, course_id, module_id, module_item_id, **kwargs):
      """
      Update this module item.

      :calls: `PUT /api/v1/courses/:course_id/modules/:module_id/items/:id \
      <https://canvas.instructure.com/doc/api/modules.html#method.context_module_items_api.update>`_

      :returns: The updated module item.
      :rtype: dict
      """
      response = self._requester.request(
         "PUT",
         "courses/{}/modules/{}/items/{}".format(
               course_id, module_id, module_item_id
         ),
         _kwargs=combine_kwargs(**kwargs),
      )
      module_item_json = response.json()
      module_item_json.update({"course_id": course_id})

      return module_item_json

   def uncomplete_module_item(self, course_id, module_id, module_item_id, **kwargs):
      """
      Mark this module item as not done.

      :calls: `DELETE /api/v1/courses/:course_id/modules/:module_id/items/:id/done \
      <https://canvas.instructure.com/doc/api/modules.html#method.context_module_items_api.mark_as_done>`_

      :rtype: dict
      """
      response = self._requester.request(
         "DELETE",
         "courses/{}/modules/{}/items/{}/done".format(
               course_id, module_id, module_item_id
         ),
         _kwargs=combine_kwargs(**kwargs),
      )
      module_item_json = response.json()
      module_item_json.update({"course_id": course_id})

      return module_item_json