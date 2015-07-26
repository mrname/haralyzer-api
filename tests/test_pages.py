"""
Tests the '/tests/' endpoint
"""

import datetime
import json
import pytest

from haralyzer.assets import HarPage
from har_api.models import Test
ENDPOINT = '/pages/'
PAGE_ID = 'page_3'

def test_get_single_page(app, test_data):
    """
    Tests ability to retrieve a single Page object with a GET request specifying
    the page ID in the query string.
    """
    data = test_data('humanssuck.net.har')
    with app.test_request_context():
        t = Test(data)
        t.save()
        # This should have saved only one page
        test_page = t.pages[0]
        res = app.client.get('{0}{1}/'.format(ENDPOINT, test_page.id))
        assert res.status_code == 200

        # Check for response data produced by the API
        res_json = json.loads(res.data.decode())
        assert 'data' in res_json
        res_data = res_json['data']
        assert res_data['hostname'] == 'humanssuck.net'

        # Check for response data produced by HarPage object
        har_page = HarPage(PAGE_ID, har_data=json.loads(data))
        for field in test_page.har_page_fields:
            assert getattr(har_page, field) == res_data[field]


@pytest.mark.xfail
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
        # Filter by hostname only
        res = app.client.get('{0}?hostname=humanssuck.net'.format(ENDPOINT))
        assert res.status_code == 200
        # Filter by test name only
        # Filter by startedDateTime only
        # Filter by hostname AND test name
        # filter by hostname AND startedDateTime
        # Filter by hostname AND test name AND startedDateTime
        # Filter by test name AND startedDateTime


def test_pages_model(app, test_data):
    """
    When a new Test object is created, it should automatically create
    corresponding page entries.
    """
    data = test_data('humanssuck.net.har')
    with app.test_request_context():
        # Create a test object which in turn makes the appropriate page
        t = Test(data)
        t.save()
        assert t.pages
        assert len(t.pages) == 1
        test_page = t.pages[0]
        assert test_page.hostname == 'humanssuck.net'
        assert test_page.test_id == t.id

        # Make sure that the object is storing whatever haralyzer.HarPage would
        # produce
        har_page = HarPage(PAGE_ID, har_data=json.loads(data))
        for field in test_page.har_page_fields:
            assert getattr(har_page, field) == getattr(test_page, field)
