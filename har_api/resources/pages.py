from flask.ext.restful import reqparse, Resource, marshal_with
from har_api.models import Page
from har_api.resource_fields import page_fields
from har_api.utils import filter_args


class HarPageSingle(Resource):
    """
    Resource for retrieving one page from a collection of HAR data.
    """
    @marshal_with(page_fields, envelope='data')
    def get(self, page_id):
        """
        Returns either a singe test with test_id or a collection based on GET
        params.

        :param test_id: ID of the test as passed in the resource URL
        :type test_id: integer
        :rtype: dict
        """
        page = Page.query.get_or_404(page_id)
        return (page, 200)


class HarPageCollection(Resource):
    """
    Resource for retrieving a collection of pages using filters.
    """
    @marshal_with(page_fields, envelope='data')
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('hostname', help='hostname filter')
        parser.add_argument('startedDateTime', help='date/time filter')
        parser.add_argument('test_name', help='test name filter')
        kwargs = parser.parse_args()
        search_query = filter_args(kwargs)

        # TODO - pagination son!
        if search_query:
            page_query = Page.query.filter_by(**search_query)
            pages = page_query.all()
        else:
            pages = Page.query.all()
        return (pages, 200)
