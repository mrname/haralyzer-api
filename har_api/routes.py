from har_api.resources.tests import HarTestSingle, HarTestCollection
from har_api.resources.pages import HarPage


def create_routes(api):
    """
    Given an instance of a Flask-RESTFul Api object, binds the routes.
    """
    api.add_resource(HarTestCollection, '/tests/')
    api.add_resource(HarTestSingle, '/tests/<int:test_id>/')
    api.add_resource(HarPage, '/pages/', '/pages/<int:page_id>/')
