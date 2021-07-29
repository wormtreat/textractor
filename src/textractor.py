"""Document Text Extractor.

This is a simple Falcon microservice which extracts text from
an uploaded file and returns the document text in JSON, without
saving anything to disk.
"""

import falcon
from falcon_multipart.middleware import MultipartMiddleware
from .text_extractor.resources import TextExtractorResource
from .health_check.resources import HealthCheckResource

def create_app():
    """Instantiate app and define routes."""
    app = falcon.API(middleware=[MultipartMiddleware()])
    # File upload route
    process_document = TextExtractorResource()
    app.add_route('/upload', process_document)

    # Health check routes
    health_check = HealthCheckResource({'status': 'OK'})
    app.add_route('/', health_check)
    app.add_route('/elb-status', health_check)

    return app
