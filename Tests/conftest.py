import pytest
import json

@pytest.fixture
def json_loader():
    """
    Loads data from JSON file
    """

    def _loader(filename, testKey=None):
        with open(filename, 'r') as f:
            print(filename)
            data = json.load(f)
            if testKey:
               data = data.get(testKey)
        return data

    return _loader