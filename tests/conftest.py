import os
import pytest
from har_api import create_app
from har_api.models import db


def pytest_runtest_setup():
    _app = app()
    with _app.test_request_context():
        db.create_all()

def pytest_runtest_teardown():
    _app = app()
    with _app.test_request_context():
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='session')
def app():
    _app = create_app()
    _app.client = _app.test_client()
    return _app


@pytest.fixture
def content_type_json():
    """
    Add header to send data as JSON
    """
    return {'Content-Type': 'application/json'}


@pytest.fixture
def test_data(request):
    """
    Given a HAR file name, returns a ``dict`` of this data from the
    corresponding file name in tests/data
    """
    data_path = os.path.abspath(__file__ + '/../data/')

    def load_doc(filename):
        full_path = os.path.join(data_path, filename)
        with open(full_path) as f:
            return f.read()
    return load_doc
