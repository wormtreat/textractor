"""Document Text Extractor.

Resource classes
"""

import falcon
import ujson

from models.text_extractor import TextExtractor
from models.health_check import HealthCheck


class TextExtractorResource(TextExtractor):
    """Resource to extract text from POSTed file and return text in JSON.
    """

    def __init__(self):
        self.extracted_text = ""

    def on_post(self, req, resp):
        """Accept file from POST request and return text in JSON."""
        if req.content_length:
            error_message = "Error"
            file_in = req.get_param('ingest')
            # Validate data
            validation_errors = self.validate_upload(file_in)
            if len(validation_errors) > 0:
                for error in validation_errors:
                    error_message += " - " + error
                resp.body = ujson.dumps({'error': error_message})
                resp.status = falcon.HTTP_400
                return
            try:
                # Extract text
                self.extracted_text = self.extract_text(file_in)
                resp.body = ujson.dumps(
                    {'extracted_text': '{}'.format(self.extracted_text)})
                resp.status = falcon.HTTP_200
            except Exception as err:
                print("ERROR: ", repr(err))
                resp.body = ujson.dumps(
                    {'error': 'An internal server error has occurred'})
                resp.status = falcon.HTTP_500
        else:
            resp.body = ujson.dumps({'error': 'No JSON was received.'})
            resp.status = falcon.HTTP_400


class HealthCheckResource(HealthCheck):
    """Resource to extract text from POSTed file and return text in JSON.
    """

    def on_get(self, _, resp):
        """Dump body."""
        resp.body = ujson.dumps(self.body)
        resp.status = falcon.HTTP_200
