"""
Tests the '/tests/' endpoint
"""

import datetime
import json
import pytest

from har_api.models import Test
ENDPOINT = '/tests/'
TEST_ID = 1


def test_post_requires_params(app):
    """
    Tests that a POST request requires params.
    """

    # Make sure that a payload is required
    resp = app.client.post(ENDPOINT)
    assert(resp.status_code == 400)


def test_post_requires_har_data_element(app):
    """
    Makes sure that the POST request requires the 'data' element
    """
    data = {'this_should_not_work': 1}
    resp = app.client.post(ENDPOINT, data=json.dumps(data))
    assert(resp.status_code == 400)

    res_json = json.loads(resp.data)
    assert 'har_data' in res_json['message']


def test_post_validates_json(app, content_type_json):
    """
    Makes sure that the API rejects invalid HAR data... yuk.
    """
    data = {'har_data': 'vassup'}
    with pytest.raises(ValueError):
        app.client.post(ENDPOINT, data=json.dumps(data),
                        headers=content_type_json)


def test_post_valid_request(app, content_type_json, test_data):
    """
    Makes sure that we can POST a valid payload to the /tests/ endpoint
    """
    payload = {'har_data': test_data('humanssuck.net.har')}
    res = app.client.post(ENDPOINT, data=json.dumps(payload),
                          headers=content_type_json)
    assert res.status_code == 200


def test_get_single_test(app, test_data):
    """
    Tests ability to retrieve a single Test object with a GET request.
    """
    data = test_data('humanssuck.net.har')
    with app.test_request_context():
        t = Test(data)
        t.save()
        res = app.client.get('{0}{1}/'.format(ENDPOINT, TEST_ID))
        assert res.status_code == 200
        res_json = json.loads(res.data)
        #assert 'data' in res_json


def test_get_test_collection(app):
    """
    Tests the ability of a GET request to obtain a collection of tests based on
    certain criteria.
    """
    # TODO - test this
    pass


def test_tests_model(app, test_data):
    """
    When a new Test object is created, it should automatically create
    corresponding page entries, as well as store some of the fields from the
    provided HAR data.
    """
    data = test_data('humanssuck.net.har')
    with app.test_request_context():
        t = Test(data)
        t.save()
        assert t.pages
        assert len(t.pages) == 1
        # TODO - test a HAR file with multiple pages
        assert t.hostname == 'humanssuck.net'
        assert t.browser_name == 'Firefox'
        assert t.browser_version == '25.0.1'
        assert t.data == data
        assert t.startedDateTime == datetime.datetime(2015, 2, 22, 19, 28, 12, 136000)
