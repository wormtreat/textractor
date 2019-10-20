import falcon
import bjoern
import ujson
import zipfile
from falcon_multipart.middleware import MultipartMiddleware

import PyPDF2

import io
import os

# Define webserver host and port
WEB_HOST = '0.0.0.0'
PORT = 8060

class GetDocumentText(object):
    def on_post(self, req, resp):
        if req.content_length:          
            text_out = ""
            error_message = "Error"
            file_in = req.get_param('ingest')
            # Validate data
            validation_errors = validate_upload(file_in)
            if len(validation_errors) > 0:
                for error in validation_errors:
                    error_message += " - " + error
                resp.body = ujson.dumps({'error': error_message})
                resp.status = falcon.HTTP_400    
                return
            try:
                # Extract text
                text_out = extract_text(file_in)
                resp.body = ujson.dumps({'extracted_text': '{}'.format(text_out)})
                resp.status = falcon.HTTP_200
            except:
                resp.body = ujson.dumps(
                    {'error': 'An internal server error has occurred'})
                resp.status = falcon.HTTP_500
        else:
            resp.body = ujson.dumps({'error': 'No JSON was received.'})
            resp.status = falcon.HTTP_400


def validate_upload(file_in):
    errors = []
    if file_in == None:
        errors.append('Error uploading file, file not found.')
    if not file_in.filename:
        errors.append('Error uploading file, filename not found.')
    extention = get_file_extention(file_in.filename)
    if not allowed_file(extention):
        errors.append('File type not allowed.')
    return errors


def extract_text(file_in):
    # print('EXTRACT')
    text_out = ""
    if type(file_in) == zipfile.ZipExtFile:
        filename = file_in.name
    else:
        filename = file_in.filename
    extention = get_file_extention(filename)
    if extention == 'zip':
        text_out = process_zip(file_in)
    elif extention == 'txt':
        text_out = process_txt(file_in)
    elif extention == 'pdf':
        text_out = process_pdf(file_in)
    return text_out


def process_zip(file_in):
    # print('ZIP File Processed')
    text_out = ""
    file_bytes = get_file_bytes(file_in)
    zip_file = zipfile.ZipFile(file_bytes,"r")
    files = zip_file.namelist()
    for filename in files:
        with zip_file.open(filename) as zippedFile:
            extention = get_file_extention(zippedFile.name)
            if allowed_file(extention):
                text_out += extract_text(zippedFile)
    return text_out


def process_txt(file_in):
    # print('TXT File Processed')
    text_out = ""
    if type(file_in) == zipfile.ZipExtFile:
        text_out = str(file_in.read(),'utf-8')
    else:
        text_out = str(file_in.file.read(),'utf-8')
    return text_out


def process_pdf(file_in):
    text_out = ""
    file_bytes = get_file_bytes(file_in)
    pdfReader = PyPDF2.PdfFileReader(file_bytes)
    for pageNumber in range(1, pdfReader.numPages):
        page = pdfReader.getPage(pageNumber)
        page_text = page.extractText()
        clean_string = (page_text.encode('ascii', 'ignore')).decode("unicode_escape")
        clean_string = os.linesep.join([s for s in clean_string.splitlines() if s])
        text_out += clean_string
    return text_out


def allowed_file(extention):
    return extention in ['txt', 'pdf', 'zip']


def get_file_extention(filename):
    split_list = filename.rsplit('.')
    return split_list[-1].lower()


def get_file_bytes(file_in):
    if not hasattr(file_in, 'file'):
        contents = file_in.read()
    else:
        contents = file_in.file.read()
    file_bytes = io.BytesIO(contents)
    return file_bytes


# Instantiate the app and resource class

# app = falcon.API()
app = falcon.API(middleware=[MultipartMiddleware()])
process_document = GetDocumentText()

# Route which accepts a Concept as JSON
app.add_route('/upload', process_document)

# Route for health checks
class HealthCheck(object):
    def on_get(self, req, resp):
        resp.body = ujson.dumps({'status': 'OK'})
        resp.status = falcon.HTTP_200

health_check = HealthCheck()
app.add_route('/', health_check)

# Run the app
bjoern.run(app, WEB_HOST, PORT)
