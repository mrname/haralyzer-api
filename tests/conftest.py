import os
import pytest
from har_api import create_app


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
