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
        Returns a single test with test_id

        :param test_id: ID of the test as passed in the resource URL
        :type test_id: integer
        :rtype: dict
        """
        test = Test.query.get_or_404(test_id)
        return (test, 200)


class HarTestCollection(Resource):
    """
    Returns a collection of HAR tests based on filters.
    """
    @marshal_with(test_fields, envelope='data')
    def get(self):
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
        Stores the raw HAR data in the tests table, and then stores one or more
        page entries in the pages table.
        """
        parser = reqparse.RequestParser()
        parser.add_argument('har_data',
                            help='har_data: String of HAR (JSON) data',
                            required=True)
        args = parser.parse_args()

        har_test = Test(data=args['har_data'])
        har_test.save()
        return (har_test, 201)
