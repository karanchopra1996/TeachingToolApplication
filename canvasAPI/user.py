from .canvas_object import CanvasObject
from .util import combine_kwargs

class User(CanvasObject):

   def get_user(self, user, **kwargs):
      """
      Retrieve a user by their ID.

      :calls: `GET /api/v1/users/:id \
      <https://canvas.instructure.com/doc/api/users.html#method.users.api_show>`_
      :param user: The user's ID or 'self'.
      :type user: int or string
      :rtype: dict
      """

      if user == "self":
         uri = "users/self"
      else:
         user_id = user
         uri = "users/{}".format(user_id)

      response = self._requester.request(
         "GET", uri, _kwargs=combine_kwargs(**kwargs)
      )
      return response.json()

   def get_profile(self, user_id, **kwargs):
      """
      Retrieve this user's profile.
      :calls: `GET /api/v1/users/:user_id/profile \
      <https://canvas.instructure.com/doc/api/users.html#method.profile.settings>`_
      :rtype: dict
      """
      response = self._requester.request(
         "GET", "users/{}/profile".format(user_id), _kwargs=combine_kwargs(**kwargs)
      )
      return response.json()