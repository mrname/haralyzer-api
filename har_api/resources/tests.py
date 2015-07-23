from flask.ext.restful import reqparse, Resource, marshal_with
from har_api.models import Test
from har_api.resource_fields import test_fields


class HarTest(Resource):
    """
    Resource for storing, retrieving, and searching raw HAR data.
    """
    @marshal_with(test_fields, envelope='data')
    def get(self, test_id=None):
        """
        Returns either a singe test with test_id or a collection based on GET
        params.

        :param test_id: ID of the test as passed in the resource URL
        :type test_id: integer
        :rtype: dict
        """
        if test_id is not None:
            test = Test.query.get_or_404(test_id)
            return (test, 200)
        else:
            parser = reqparse.RequestParser()
            parser.add_argument('hostname', help='hostname filter')
            parser.add_argument('startedDateTime', help='date/time filter')
            parser.add_argument('name', help='test name filter')
            kwargs = parser.parse_args()
            tests = Test.query.filter(**kwargs)
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
