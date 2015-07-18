import requests

def test_base():
    """
    Tests the base of the API to ensure a 200
    """
    r = requests.get('http://127.0.0.1:5000/')
    r.raise_for_status()
