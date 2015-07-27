from flask.ext.restful import reqparse, Resource, marshal_with, marshal
from har_api.models import Test
from har_api.resource_fields import test_fields
from har_api.utils import filter_args


class HarTestSingle(Resource):
    """
    Resource for storing HAR data or retriveing a single test by ID
    """
    @marshal_with(test_fields, envelope='data')
    def get(self, test_id):
        """
        Returns a single test object (representing a HAR file of a full test
        run) with test_id.

        **Example request**:

            .. sourcecode:: http

                GET /tests/123/ HTTP/1.1
                Host: har-api.com
                Accept: application/json, text/javascript

        **Example response**:

            .. sourcecode:: http

                HTTP/1.1 200 OK
                Vary: accept
                Content-Type: text/javascript

                {
                    "data": {
                        "browser_name": "Firefox",
                        "browser_version": "25.0.1",
                        "hostname": "humanssuck.net",
                        "name": null,
                        "pages": [
                            {
                                "audio_load_time": 0.0,
                                .... see page object for details .....
                                "video_size": 0.0
                            }
                        ],
                        "startedDateTime": "Sun, 22 Feb 2015 19:28:12 -0000"
                    }
                }

        :>json integer id: System assigned ID
        :>json string browser_name: Name of browser used for test
        :>json string browser_version: Browser version used for test
        :>json string hostname: Hostname of the test
        :>json string name: Custom test name
        :>json array pages: An array of page objects
        :>json startedDateTime: Start date/time of the test run

        :statuscode 200: I haz test 4 u
        :statuscode 404: test not found
        :statuscode 500: internal error
        """
        test = Test.query.get_or_404(test_id)
        return (test, 200)


class HarTestCollection(Resource):
    """
    Returns a collection of HAR tests based on filters.
    """
    def get(self):
        """
        Returns a collection of HAR tests based on filters.

        **Example request**:

        .. sourcecode:: http

            GET /tests/?hostname=humanssuck.net HTTP/1.1
            Host: har-api.com
            Accept: application/json, text/javascript

        **Example response**:

        .. sourcecode:: http

           HTTP/1.1 200 OK
           Vary: accept
           Content-Type: text/javascript

        :query hostname: Hostname of the test
        :query startedDateTime: Date the test was run on
        :query name: Custom name for the tests

        :statuscode 200: You've got tests!
        :statuscode 500: internal error
        """
        pagination_vals = ['page', 'limit']

        parser = reqparse.RequestParser()
        parser.add_argument('hostname', help='hostname filter')
        parser.add_argument('startedDateTime', help='date/time filter')
        parser.add_argument('name', help='test name filter')
        parser.add_argument('page', default=1, type=int,
                            help='page for pagination')
        parser.add_argument('limit', default=100, type=int,
                            help='limit for pagination')

        kwargs = parser.parse_args()
        search_query = filter_args(kwargs)

        pagination_args = {}
        for val in pagination_vals:
            pagination_args[val] = search_query[val]
            del search_query[val]

        print pagination_args
        # TODO - pagination son!
        if search_query:
            test_query = Test.query.filter_by(**search_query)
        else:
            test_query = Test.query

        tests_paginated = test_query.paginate(pagination_args['page'],
                                              pagination_args['limit'])

        tests_data = marshal(tests_paginated.items, test_fields)
        resp = {'data':
                {'tests': tests_data},
                'total': tests_paginated.total,
                'page': pagination_args['page'],
                'limit': pagination_args['limit'],
                }
        return (resp, 200)

    @marshal_with(test_fields, envelope='data')
    def post(self):
        """
        Given a string of HAR data, creates a new 'test' entry (as well as it's
        corresponding 'page' resources).

        **Example request**:

        .. sourcecode:: http

            POST /tests/ HTTP/1.1
            Host: har-api.com
            Accept: application/json, text/javascript

            {
                "har_data": "{"log": {"pages": [{"id": "page_3", ......."
            }

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: accept
            Content-Type: text/javascript

            {
                "data": {
                    "browser_name": "Firefox",
                    "browser_version": "25.0.1",
                    "hostname": "humanssuck.net",
                    "name": null,
                    "pages": [
                        {
                            "audio_load_time": 0.0,
                            .... see page object for details .....
                            "video_size": 0.0
                        }
                    ],
                    "startedDateTime": "Sun, 22 Feb 2015 19:28:12 -0000"
                }
            }

        :<json string har_data: Raw HAR data (JSON)
        :<json string name: A custom name for the test, which can be used later
            for searching

        :>json integer id: System assigned ID
        :>json string browser_name: Name of browser used for test
        :>json string browser_version: Browser version used for test
        :>json string hostname: Hostname of the test
        :>json string name: Custom test name
        :>json array pages: An array of page objects
        :>json startedDateTime: Start date/time of the test run

        :statuscode 201: Test created without issue
        :statuscode 500: internal error
        """
        parser = reqparse.RequestParser()
        parser.add_argument('har_data',
                            help='har_data: String of HAR (JSON) data',
                            required=True)
        args = parser.parse_args()

        har_test = Test(data=args['har_data'])
        har_test.save()
        return (har_test, 201)
