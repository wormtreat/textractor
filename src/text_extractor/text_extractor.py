"""Document Text Extractor.

TextExtracor class
"""
import io
import os
import zipfile
import PyPDF2


class TextExtractor(object):
    """Extract text from file and return it in JSON.
    """
    extracted_text = ""
    allowed_extensions = ['txt', 'pdf', 'zip']

    def __init__(self):
        self.extracted_text = ""

    def validate_upload(self, file_in):
        """Validate file type is accepted."""
        errors = []
        if file_in == None:
            errors.append('Error uploading file, file not found.')
        if not file_in.filename:
            errors.append('Error uploading file, filename not found.')
        extension = self.get_file_extension(file_in.filename)
        if not self.allowed_file(extension):
            errors.append('File type not allowed.')
        return errors

    def extract_text(self, file_in):
        """Extract text from file based on file extension."""
        if type(file_in) == zipfile.ZipExtFile:
            filename = file_in.name
        else:
            filename = file_in.filename
        extension = self.get_file_extension(filename)
        if extension == 'zip':
            self.extracted_text = self.process_zip(file_in)
        elif extension == 'txt':
            self.extracted_text = self.process_txt(file_in)
        elif extension == 'pdf':
            self.extracted_text = self.process_pdf(file_in)
        return self.extracted_text

    def process_zip(self, file_in):
        """Extract text from zip file."""
        file_bytes = self.get_file_bytes(file_in)
        zip_file = zipfile.ZipFile(file_bytes, "r")
        files = zip_file.namelist()
        for filename in files:
            with zip_file.open(filename) as zippedFile:
                extension = self.get_file_extension(zippedFile.name)
                if self.allowed_file(extension):
                    self.extracted_text += self.extract_text(zippedFile)
        return self.extracted_text

    def process_txt(self, file_in):
        """Extract text from text file."""
        if type(file_in) == zipfile.ZipExtFile:
            self.extracted_text = str(file_in.read(), 'utf-8')
        else:
            self.extracted_text = str(file_in.file.read(), 'utf-8')
        return self.extracted_text

    def process_pdf(self, file_in):
        """Extract text from pdf file."""
        file_bytes = self.get_file_bytes(file_in)
        pdfReader = PyPDF2.PdfFileReader(file_bytes)
        for pageNumber in range(1, pdfReader.numPages):
            page = pdfReader.getPage(pageNumber)
            page_text = page.extractText()
            clean_string = (page_text.encode('ascii', 'ignore')
                            ).decode("unicode_escape")
            clean_string = os.linesep.join(
                [s for s in clean_string.splitlines() if s])
            self.extracted_text += clean_string
        return self.extracted_text

    def allowed_file(self, extension):
        """Return allowed file extensions."""
        return extension in self.allowed_extensions

    def get_file_extension(self, filename):
        """Return file extension."""
        split_list = filename.rsplit('.')
        return split_list[-1].lower()

    def get_file_bytes(self, file_in):
        """Return file bytes."""
        if not hasattr(file_in, 'file'):
            contents = file_in.read()
        else:
            contents = file_in.file.read()
        file_bytes = io.BytesIO(contents)
        return file_bytes
