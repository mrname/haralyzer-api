from flask.ext.restful import reqparse, Resource, marshal_with
from har_api.models import Page
from har_api.resource_fields import page_fields


class HarPage(Resource):
    """
    Resource for retrieving one or more pages from a collection of HAR data.
    """
    @marshal_with(page_fields, envelope='data')
    def get(self, page_id=None):
        """
        Returns either a singe test with test_id or a collection based on GET
        params.

        :param test_id: ID of the test as passed in the resource URL
        :type test_id: integer
        :rtype: dict
        """
        if page_id is not None:
            page = Page.query.get_or_404(page_id)
            return (page, 200)
        else:
            parser = reqparse.RequestParser()
            parser.add_argument('test_id', help='hostname filter')
            parser.add_argument('startedDateTime', help='date/time filter')
            parser.add_argument('test_name', help='test name filter')
            kwargs = parser.parse_args()
            pages = Page.query.filter(**kwargs)
            return (pages, 200)
