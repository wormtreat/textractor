"""Document Text Extractor.

TextExtracor class
"""
import io
import os
import zipfile
import PyPDF2


class TextExtractor():
    """Extract text from file and return it in JSON.
    """
    extracted_text = ""
    allowed_extensions = ['txt', 'pdf', 'zip']
    uploaded_file = None

    def set_uploaded_file(self, uploaded_file):
        """Set file to ingest."""
        self.uploaded_file = uploaded_file

    def validate_filename(self):
        """Validate file type is accepted."""
        errors = []
        if self.uploaded_file is None:
            errors.append('Error uploading file, file not found.')
        if not self.uploaded_file.filename:
            errors.append('Error uploading file, filename not found.')
        extension = self.get_file_extension(self.uploaded_file.filename)
        if not self.allowed_file(extension):
            errors.append('File type not allowed.')
        return errors

    def extract_text(self):
        """Extract text from file based on file extension."""
        if isinstance(self.uploaded_file, (zipfile.ZipExtFile)):
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
        text_out = ""
        file_bytes = self.get_file_bytes()
        with zipfile.ZipFile(file_bytes, "r") as zip_file:
            files = zip_file.namelist()
            for filename in files:
                with zip_file.open(filename) as zipped_file:
                    extension = self.get_file_extension(zipped_file.name)
                    if self.allowed_file(extension):
                        self.uploaded_file = zipped_file
                        text_out += self.extract_text()
        return text_out

    def process_txt(self):
        """Extract text from text file."""
        text_out = ""
        if isinstance(self.uploaded_file, (zipfile.ZipExtFile)):
            text_out = str(self.uploaded_file.read(), 'utf-8')
        else:
            text_out = str(self.uploaded_file.file.read(), 'utf-8')
        return text_out

    def process_pdf(self):
        """Extract text from pdf file."""
        text_out = ""
        file_bytes = self.get_file_bytes()
        pdf_reader = PyPDF2.PdfFileReader(file_bytes)
        for page_number in range(0, pdf_reader.numPages):
            page = pdf_reader.getPage(page_number)
            page_text = page.extractText()
            clean_string = (page_text.encode('ascii', 'ignore')
                            ).decode("unicode_escape")
            clean_string = os.linesep.join(
                [s for s in clean_string.splitlines() if s])
            text_out += clean_string
        return text_out

    def allowed_file(self, extension):
        """Return allowed file extensions."""
        return extension in self.allowed_extensions

    def get_file_bytes(self):
        """Return file bytes."""
        if not hasattr(self.uploaded_file, 'file'):
            contents = self.uploaded_file.read()
        else:
            contents = self.uploaded_file.file.read()
        file_bytes = io.BytesIO(contents)
        return file_bytes

    @staticmethod
    def get_file_extension(filename):
        """Return file extension."""
        split_list = filename.rsplit('.')
        return split_list[-1].lower()
