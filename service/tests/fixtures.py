"""Document Text Extractor.

Test fixtures
"""


import os
import pytest
from falcon import testing
from ..src.textractor import create_app


@pytest.fixture()
def client():
    """Client fixture."""
    return testing.TestClient(create_app())


@pytest.fixture()
def text_file():
    """Text file fixture."""
    return get_file_info('test_text.txt')


@pytest.fixture()
def zip_file():
    """Zip file fixture."""
    return get_file_info('test_text.zip')


@pytest.fixture()
def nested_zip_file():
    """Nested zip file fixture."""
    return get_file_info('test_text_nested.zip')


@pytest.fixture()
def pdf_file():
    """PDF file fixture."""
    return get_file_info('test_text.pdf')


def get_file_info(test_file):
    """File metadata."""
    test_folder = 'test_data/'
    test_path = test_folder + test_file
    here = os.path.dirname(os.path.realpath(__file__))
    filepath = os.path.join(here, test_path)

    with open(filepath, 'rb') as open_file:
        file_text = open_file.read()

    file_info = {
        'folder': test_folder,
        'file': test_file,
        'path': filepath,
        'data': file_text
    }
    return file_info
