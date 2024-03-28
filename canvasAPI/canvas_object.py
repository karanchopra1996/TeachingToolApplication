from . import requester

class CanvasObject(object):
   """
   Base class for all classes representing objects returned by the API.

   """

   def __init__(self, requester):
      """
      :param requester: The requester to pass HTTP requests through.
      :type requester: :class:`core.requester.Requester`
      :param response: The JSON object
      :type response: dict
      """
      self._requester = requester

   def __repr__(self):  # pragma: no cover
      classname = self.__class__.__name__
      return "{}".format(classname)
