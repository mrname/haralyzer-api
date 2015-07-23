"""
A home for happy little utility functions.
"""
import json


def filter_json(data):
    """
    Helper function that returns either the decoded valid of a JSON string or
    NONE if the string is not valid JSON.
    """
    try:
        res = json.loads(data)
        return res
    except (ValueError, TypeError):
        return None
