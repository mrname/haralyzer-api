from flask.ext.restful import reqparse, Resource
from har_api.models import Test

parser = reqparse.RequestParser()

parser.add_argument('har_data', help='har_data: String of HAR (JSON) data',
                    required=True)


class HarTest(Resource):
    """
    Resource for storing, retrieving, and searching raw HAR data.
    """
    def get(self, test_id):
        """
        Returns either a singe test with test_id or a collection based on GET
        params.

        :param test_id: ID of the test as passed in the resource URL
        :type test_id: integer
        :rtype: dict
        """
        if test_id:
            test = Test.query.get_or_404(test_id)
            return test.to_dict()
        else:
            # TODO - Add GET filters here
            pass

    def post(self):
        """
        Stores the raw HAR data in the tests table, and then stores one or more
        page entries in the pages table.
        """
        args = parser.parse_args()

        har_test = Test(data=args['har_data'])
        har_test.save()
        return har_test.to_dict()
