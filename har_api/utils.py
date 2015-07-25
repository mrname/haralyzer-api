"""
A home for happy little utility functions.
"""
import json
import six

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

def filter_args(args):
    """
    A small helper function that takes a ``dict`` of args (as created by
    reqparse.parse_args() and returns a ``dict`` with the empty args removed.
    This is allows us to directly pass the arguments using 'filter_by' queries
    :param args: ``dict`` of arguments
    :type args: dict[string, object]
    :returns: ``dict`` of arguments with any blank args removed
    :rtype: dict[string, object]
    """
    return dict(filter(lambda x: x[1], six.iteritems(args)))
