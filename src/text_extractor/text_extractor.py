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
    uploaded_file = None

    def set_uploaded_file(self, uploaded_file):
        self.uploaded_file = uploaded_file

    def validate_filename(self):
        """Validate file type is accepted."""
        errors = []
        if self.uploaded_file == None:
            errors.append('Error uploading file, file not found.')
        if not self.uploaded_file.filename:
            errors.append('Error uploading file, filename not found.')
        extension = self.get_file_extension(self.uploaded_file.filename)
        if not self.allowed_file(extension):
            errors.append('File type not allowed.')
        return errors

    def extract_text(self):
        """Extract text from file based on file extension."""
        if type(self.uploaded_file) == zipfile.ZipExtFile:
            filename = self.uploaded_file.name
        else:
            filename = self.uploaded_file.filename
        extension = self.get_file_extension(filename)
        if extension == 'zip':
            self.extracted_text = self.process_zip()
        elif extension == 'txt':
            self.extracted_text = self.process_txt()
        elif extension == 'pdf':
            self.extracted_text = self.process_pdf()
        return self.extracted_text

    def process_zip(self):
        """Extract text from zip file."""
        file_bytes = self.get_file_bytes()
        zip_file = zipfile.ZipFile(file_bytes, "r")
        files = zip_file.namelist()
        for filename in files:
            with zip_file.open(filename) as zippedFile:
                extension = self.get_file_extension(zippedFile.name)
                if self.allowed_file(extension):
                    self.extracted_text += self.extract_text(zippedFile)
        return self.extracted_text

    def process_txt(self):
        """Extract text from text file."""
        if type(self.uploaded_file) == zipfile.ZipExtFile:
            self.extracted_text = str(self.uploaded_file.read(), 'utf-8')
        else:
            self.extracted_text = str(self.uploaded_file.file.read(), 'utf-8')
        return self.extracted_text

    def process_pdf(self):
        """Extract text from pdf file."""
        file_bytes = self.get_file_bytes()
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

    def get_file_bytes(self):
        """Return file bytes."""
        if not hasattr(self.uploaded_file, 'file'):
            contents = self.uploaded_file.read()
        else:
            contents = self.uploaded_file.file.read()
        file_bytes = io.BytesIO(contents)
        return file_bytes
