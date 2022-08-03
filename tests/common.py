"""Define common test utilities."""
import os

TEST_LATITUDE = 40.7152
TEST_LONGITUDE = -73.9877


def load_fixture(filename):
    """Load a fixture."""
    path = os.path.join(os.path.dirname(__file__), "fixtures", filename)
    with open(path, encoding="utf-8") as fptr:
        return fptr.read()
