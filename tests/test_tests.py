"""
Tests the '/tests/' endpoint
"""

import datetime
import json
import pytest

from har_api.models import Test
ENDPOINT = '/tests/'


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

    res_json = json.loads(resp.data.decode())
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
    assert res.status_code == 201
    res_json = json.loads(res.data.decode())
    assert 'data' in res_json


def test_get_single_test(app, test_data):
    """
    Tests ability to retrieve a single Test object with a GET request.
    """
    data = test_data('humanssuck.net.har')
    with app.test_request_context():
        t = Test(data, name='my_test')
        t.save()
        res = app.client.get('{0}{1}/'.format(ENDPOINT, t.id))
        assert res.status_code == 200
        res_json = json.loads(res.data.decode())
        assert 'data' in res_json
        res_data = res_json['data']
        assert res_data['hostname'] is not None
        assert res_data['name'] is not None
        assert res_data['browser_name'] is not None
        assert res_data['startedDateTime'] is not None
        assert 'pages' in res_data
        res_pages = res_data['pages']
        assert len(res_pages) == 1


def test_get_test_collection(app, test_data):
    """
    Tests the ability of a GET request to obtain a collection of tests based on
    certain criteria.
    """
    hs_data = test_data('humanssuck.net.har')
    cnn_data = test_data('cnn.com.har')
    with app.test_request_context():
        t1 = Test(hs_data, name='hs_test_1')
        t1.save()
        t2 = Test(hs_data, name='hs_test_2')
        t2.save()
        t3 = Test(cnn_data, name='hs_test_1')
        t3.save()
        # Get all of them
        res = app.client.get(ENDPOINT)
        assert res.status_code == 200
        res_json = json.loads(res.data.decode())
        assert 'data' in res_json
        res_data = res_json['data']


        # Filter by hostname only
        res = app.client.get('{0}?hostname=humanssuck.net'.format(ENDPOINT))
        assert res.status_code == 200
        res_json = json.loads(res.data.decode())
        assert 'data' in res_json
        res_data = res_json['data']
        # Filter by test name only
        # Filter by startedDateTime only
        # Filter by hostname AND test name
        # filter by hostname AND startedDateTime
        # Filter by hostname AND test name AND startedDateTime
        # Filter by test name AND startedDateTime


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
        # MySQL does not store microseconds
        test_time = t.startedDateTime.replace(microsecond=0)
        assert test_time == datetime.datetime(2015, 2, 22, 19, 28, 12)
        assert t.har_data.decode() == data
