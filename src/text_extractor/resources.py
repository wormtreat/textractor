"""Document Text Extractor.

Resource classes
"""

import falcon

from .text_extractor import TextExtractor


class TextExtractorResource(TextExtractor):
    """Resource to extract text from POSTed file and return text in JSON.
    """

    def on_post(self, req, resp):
        """Accept file from POST request and return text in JSON."""
        if req.content_length:
            error_message = "Error"
            # Set input file
            self.set_uploaded_file(req.get_param('ingest'))
            # Validate data
            validation_errors = self.validate_filename()
            if len(validation_errors) > 0:
                for error in validation_errors:
                    error_message += " - " + error
                resp.media = {'error': error_message}
                resp.status = falcon.HTTP_400
                return
            try:
                # Extract text
                self.extracted_text = self.extract_text()
                resp.media = {'extracted_text': '{}'.format(
                    self.extracted_text)}
                resp.status = falcon.HTTP_200
            except Exception as err:
                print("ERROR: ", repr(err), flush=True)
                resp.media = {'error': 'An internal server error has occurred'}
                resp.status = falcon.HTTP_500
        else:
            resp.media = {'error': 'No JSON was received.'}
            resp.status = falcon.HTTP_400
