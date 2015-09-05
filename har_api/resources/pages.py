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
        Returns a single page object (representing one page of a HAR test)
        specified by page_id.

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

                "data": {
                    audio_load_time: 0,
                    audio_size: 0,
                    css_load_time: 76,
                    css_size: 8,
                    hostname: "humanssuck.net",
                    html_load_time: 153,
                    id: 1,
                    image_load_time: 304,
                    image_size: 23591,
                    js_load_time: 310,
                    js_size: 38367,
                    page_id: "page_3",
                    page_load_time: 567,
                    page_size: 62204,
                    startedDateTime: "Sun, 22 Feb 2015 19:28:12 -0000",
                    test_id: 2,
                    text_size: 246,
                    time_to_first_byte: 153,
                    url: "http://humanssuck.net/",
                    video_load_time: 0,
                    video_size: 0
                },
                        ............................

        :>json integer audio_load_time: Total load time for audio files (ms)
        :>json integer css_load_time: Total load time for CSS files (ms)
        :>json integer css_size: Total size of CSS assets (kb)
        :>json string hostname: Hostname of the page request
        :>json integer html_load_time: Total load time for HTML files (ms)
        :>json integer id: System assigned id
        :>json integer image_load_time: Total load time for image files (ms)
        :>json integer image_size: Total size of image assets (kb)
        :>json integer js_load_time: Total load time for javascript files (ms)
        :>json integer js_size: Total size of javascript assets (ms)
        :>json string page_id: Page ID as specified in the HAR file
        :>json integer page_load_time: Total page load time (ms)
        :>json integer page_size: Total page size (kb)
        :>json string startedDateTime: Start date/time of the test
        :>json integer test_id: System assigned ID of parent test
        :>json integer text_size: Total size of all text assets (kb)
        :>json integer time_to_first_byte: Time to first byte (ms)
        :>json string url: Canonical URL of page request
        :>json integer video_load_time: Total load time of videos assets (ms)
        :>json integer video_size: Total size of loaded video files (kb)

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
        :query name: Custom name for the test containing this page
        :statuscode 200: You've got tests!
        :statuscode 500: internal error
        """
        parser = reqparse.RequestParser()
        parser.add_argument('hostname', help='hostname filter')
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
