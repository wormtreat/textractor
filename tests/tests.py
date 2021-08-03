"""Document Text Extractor.

Pytest tests
"""

import cgi
from falcon import falcon

from ..src.text_extractor.text_extractor import TextExtractor
from .fixtures import client, text_file, zip_file, pdf_file, nested_zip_file
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


def test_validate_filename(text_file):
    """Test validating uploaded file."""
    textractor = TextExtractor()
    textractor.uploaded_file = cgi.FieldStorage()
    textractor.uploaded_file.filename = text_file['file']

    assert textractor.validate_filename() == []


def test_extract_text(text_file):
    """Test extracting text from text file."""
    textractor = TextExtractor()
    textractor.uploaded_file = cgi.FieldStorage()
    textractor.uploaded_file.filename = text_file['file']

    filepath = text_file['path']

    with open(filepath, 'rb') as f:
        textractor.uploaded_file.file = f
        assert textractor.extract_text() == 'Hi, this is test text.'


def test_extract_text_from_pdf(pdf_file):
    """Test extracting text from pdf file."""
    textractor = TextExtractor()
    textractor.uploaded_file = cgi.FieldStorage()
    textractor.uploaded_file.filename = pdf_file['file']

    filepath = pdf_file['path']

    with open(filepath, 'rb') as f:
        textractor.uploaded_file.file = f
        assert textractor.extract_text() == 'Hi, this is test text.'


def test_extract_text_from_zip(zip_file):
    """Test extracting text from zip file."""
    textractor = TextExtractor()
    textractor.uploaded_file = cgi.FieldStorage()
    textractor.uploaded_file.filename = zip_file['file']

    filepath = zip_file['path']

    with open(filepath, 'rb') as f:
        textractor.uploaded_file.file = f
        assert textractor.extract_text() == 'Hi, this is test text.'


def test_extract_text_from_nested_zip(nested_zip_file):
    """Test extracting text from text file in a zip, within a zip."""
    textractor = TextExtractor()
    textractor.uploaded_file = cgi.FieldStorage()
    textractor.uploaded_file.filename = nested_zip_file['file']

    filepath = nested_zip_file['path']

    with open(filepath, 'rb') as f:
        textractor.uploaded_file.file = f
        assert textractor.extract_text() == 'Hi, this is test text.'

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
