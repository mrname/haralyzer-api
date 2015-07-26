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
        Returns either a single page object (representing one page of a HAR
        test) specified by page_id.

        **Example request**:

            .. sourcecode:: http

                GET /pages/123/ HTTP/1.1
                Host: har-api.com
                Accept: application/json, text/javascript

        **Example response**:

            .. sourcecode:: http

                HTTP/1.1 200 OK
                Vary: accept
                Content-Type: text/javascript

        :statuscode 200: I haz page 4 u
        :statuscode 404: page not found
        :statuscode 500: internal error
        """
        page = Page.query.get_or_404(page_id)
        return (page, 200)


class HarPageCollection(Resource):
    """
    Resource for retrieving a collection of pages using filters.
    """
    @marshal_with(page_fields, envelope='data')
    def get(self):
        """
        Retrieve a collection of pages based on filter critieria
        **Example request**:

        .. sourcecode:: http

            GET /pages/?hostname=humanssuck.net HTTP/1.1
            Host: har-api.com
            Accept: application/json, text/javascript

        **Example response**:

        .. sourcecode:: http

           HTTP/1.1 200 OK
           Vary: accept
           Content-Type: text/javascript

        :query hostname: Hostname of the page
        :query startedDateTime: Date/time of the page scan run
        :query name: Custom name for the test containing this page
        :statuscode 200: You've got tests!
        :statuscode 500: internal error
        """
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
