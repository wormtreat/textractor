"""Document Text Extractor.

Test fixtures
"""
from ..src.textractor import create_app
import pytest
import os
from falcon import testing


@pytest.fixture()
def client():
    return testing.TestClient(create_app())

@pytest.fixture()
def text_file():
    return get_file_info('test_text.txt')

@pytest.fixture()
def zip_file():
    return get_file_info('test_text.zip')

@pytest.fixture()
def nested_zip_file():
    return get_file_info('test_text_nested.zip')

@pytest.fixture()
def pdf_file():
    return get_file_info('test_text.pdf')

def get_file_info(test_file):
    test_folder = 'test_data/'
    test_path = test_folder + test_file
    here = os.path.dirname(os.path.realpath(__file__))
    filepath = os.path.join(here, test_path)

    with open(filepath, 'rb') as f:
        file_text = f.read()

    file_info = {
        'folder': test_folder,
        'file': test_file,
        'path': filepath,
        'data': file_text
    }
    return file_info
