"""Document Text Extractor.

Test fixtures
"""
from ..textractor import Textractor
import pytest
import os
from falcon import testing


@pytest.fixture()
def client():
    return testing.TestClient(Textractor.create_app())


@pytest.fixture()
def text_file():
    test_folder = 'test_data/'
    test_file = 'test_text.txt'
    test_path = test_folder + test_file
    here = os.path.dirname(os.path.realpath(__file__))
    filepath = os.path.join(here, test_path)

    with open(filepath, 'rb') as f:
        test_text = f.read()

    test_text = {
        'folder': test_folder,
        'file': test_file,
        'path': filepath,
        'data': test_text
    }
    return test_text
