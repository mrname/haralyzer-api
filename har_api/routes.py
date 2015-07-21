from har_api.resources.tests import HarTest


def create_routes(api):
    """
    Given an instance of a Flask-RESTFul Api object, binds the routes.
    """
    api.add_resource(HarTest, '/tests/', '/tests/<int:test_id>/')
