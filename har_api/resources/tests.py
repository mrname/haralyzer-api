from flask.ext.restful import reqparse, Resource
from har_api.models import Test

parser = reqparse.RequestParser()

parser.add_argument('har_data', help='har_data: String of HAR (JSON) data',
                    required=True)


class HarTest(Resource):
    """
    Resource for receiving raw HAR data.
    """
    def post(self):
        """
        Stores the raw HAR data in the tests table, and then stores one or more
        page entries in the pages table.
        """
        args = parser.parse_args()

        har_test = Test(data=args['har_data'])
        har_test.save()
        return har_test.to_dict()
