"""
Tests for utility functions.
"""
from har_api.utils import filter_json


def test_filter_json():
    """
    Tests har_api.utils.filter_json
    """
    assert filter_json('test') is None
    assert filter_json(1) is None
    assert filter_json({'test': 1}) is None
    assert filter_json('{"invalid_json"}') is None
    assert filter_json('{"valid_json": "1"}') is not None
