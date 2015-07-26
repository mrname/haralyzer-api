from flask.ext.restful import reqparse, Resource, marshal_with
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
    @marshal_with(test_fields, envelope='data')
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
        parser = reqparse.RequestParser()
        parser.add_argument('hostname', help='hostname filter')
        parser.add_argument('startedDateTime', help='date/time filter')
        parser.add_argument('name', help='test name filter')
        kwargs = parser.parse_args()
        search_query = filter_args(kwargs)

        # TODO - pagination son!
        if search_query:
            test_query = Test.query.filter_by(**search_query)
            tests = test_query.all()
        else:
            tests = Test.query.all()
        return (tests, 200)

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
