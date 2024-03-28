from .canvas_object import CanvasObject
from .paginated_list import PaginatedList
from .util import combine_kwargs


class Page(CanvasObject):

    def delete(self, course_id, page_url, **kwargs):
        """
        Delete this page.

        :calls: `DELETE /api/v1/courses/:course_id/pages/:url \
        <https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.destroy>`_

        :rtype: dict
        """
        response = self._requester.request(
            "DELETE",
            "courses/{}/pages/{}".format(course_id, page_url),
            _kwargs=combine_kwargs(**kwargs),
        )
        return response.json()

    def edit(self, course_id, page_url, parent_type, parent_id, **kwargs):
        """
        Update the title or the contents of a specified wiki
        page.

        :calls: `PUT /api/v1/courses/:course_id/pages/:url \
        <https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.update>`_

        :rtype: :class:`core.page.Page`
        """
        response = self._requester.request(
            "PUT",
            "{}s/{}/pages/{}".format(parent_type, parent_id, page_url),
            _kwargs=combine_kwargs(**kwargs),
        )

        page_json = response.json()
        page_json.update({"course_id": course_id})
        return page_json

    def get_parent(self, parent_type, parent_id, **kwargs):
        """
        Return the object that spawned this page.

        :calls: `GET /api/v1/groups/:group_id \
            <https://canvas.instructure.com/doc/api/groups.html#method.groups.show>`_
            or :calls: `GET /api/v1/courses/:id \
            <https://canvas.instructure.com/doc/api/courses.html#method.courses.show>`_

        :rtype: dict
        """
        response = self._requester.request(
            "GET",
            "{}s/{}".format(parent_type, parent_id),
            _kwargs=combine_kwargs(**kwargs),
        )

        return response.json()


    def get_revision_by_id(self, page_id, page_url, parent_type, parent_id, revision_id, **kwargs):
        """
        Retrieve the contents of the revision by the id.

        :calls: `GET /api/v1/courses/:course_id/pages/:url/revisions/:revision_id \
        <https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.show_revision>`_

        :returns: Contents of the page revision.
        :rtype: :dict
        """

        response = self._requester.request(
            "GET",
            "{}s/{}/pages/{}/revisions/{}".format(
                parent_type, parent_id, page_url, revision_id
            ),
            _kwargs=combine_kwargs(**kwargs),
        )
        pagerev_json = response.json()
        if self.parent_type == "group":
            pagerev_json.update({"group_id": page_id})
        elif self.parent_type == "course":
            pagerev_json.update({"course_id": page_id})

        return pagerev_json

    def get_revisions(self, page_url, parent_type, parent_id, **kwargs):
        """
        List the revisions of a page.

        :calls: `GET /api/v1/courses/:course_id/pages/:url/revisions \
        <https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.revisions>`_

        :rtype: :class:`core.paginated_list.PaginatedList`
        """
        return PaginatedList(
            self._requester,
            "GET",
            "{}s/{}/pages/{}/revisions".format(
                parent_type, parent_id, page_url
            ),
            _kwargs=combine_kwargs(**kwargs),
        )

    def revert_to_revision(self, page_url, parent_type, parent_id, revision_id, **kwargs):
        """
        Revert the page back to a specified revision.

        :calls: `POST /api/v1/courses/:course_id/pages/:url/revisions/:revision_id \
        <https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.revert>`_

        :returns: Contents of the page revision.
        :rtype: dict
        """

        response = self._requester.request(
            "POST",
            "{}s/{}/pages/{}/revisions/{}".format(
                parent_type, parent_id, page_url, revision_id
            ),
            _kwargs=combine_kwargs(**kwargs),
        )
        pagerev_json = response.json()
        pagerev_json.update({"{parent_type}_id": parent_id})

        return pagerev_json

    def show_latest_revision(self, page_url, parent_type, parent_id, **kwargs):
        """
        Retrieve the contents of the latest revision.

        :calls: `GET /api/v1/courses/:course_id/pages/:url/revisions/latest \
        <https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.show_revision>`_

        :rtype: dict
        """
        response = self._requester.request(
            "GET",
            "{}s/{}/pages/{}/revisions/latest".format(
                parent_type, parent_id, page_url
            ),
            _kwargs=combine_kwargs(**kwargs),
        )
        return response.json()
