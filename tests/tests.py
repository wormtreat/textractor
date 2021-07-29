"""Document Text Extractor.

Pytest tests
"""

from falcon import falcon
import cgi

from ..models.text_extractor import TextExtractor
from .fixtures import client, text_file
from .utils import create_multipart

# --- --- ---
# Unit Tests
# --- --- ---


def test_allowed_file():
    """Test allowed file extensions."""
    textractor = TextExtractor()
    assert textractor.allowed_file("zip") == True
    assert textractor.allowed_file("txt") == True
    assert textractor.allowed_file("pdf") == True
    assert textractor.allowed_file("jpg") == False


def test_validate_upload(text_file):
    """Test validating uploaded file."""
    textractor = TextExtractor()

    data = cgi.FieldStorage()
    data.filename = text_file['file']
    assert textractor.validate_upload(data) == []


def test_extract_text(text_file):
    """Test extracting text from file."""
    textractor = TextExtractor()

    data = cgi.FieldStorage()
    data.filename = text_file['file']

    filepath = text_file['path']
    with open(filepath, 'rb') as f:
        data.file = f
        assert textractor.extract_text(data) == 'Hi, this is test text.'

# --- --- ---
# Endpoint Tests
# --- --- ---


def test_healthcheck(client):
    """Test healthcheck endpoints."""
    result = client.simulate_get('/')
    assert result.status == falcon.HTTP_OK
    assert result.json['status'] == 'OK'

    result = client.simulate_get('/elb-status')
    assert result.status == falcon.HTTP_OK
    assert result.json['status'] == 'OK'


def test_file_upload(client, text_file):
    """Test uploading text file."""
    # Create the multipart data
    data, headers = create_multipart(text_file['data'], fieldname='ingest',
                                    filename=text_file['file'],
                                    content_type='plain/text')
    # Post to endpoint
    result = client.simulate_request(method='POST', path="/upload",
                                    headers=headers, body=data)
    assert result.status == falcon.HTTP_OK
    assert result.json['extracted_text'] == 'Hi, this is test text.'
