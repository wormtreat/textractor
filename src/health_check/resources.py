"""Document Text Extractor.

Resource classes
"""

import falcon
import ujson

from .health_check import HealthCheck

class HealthCheckResource(HealthCheck):
    """Resource to extract text from POSTed file and return text in JSON.
    """

    def on_get(self, _, resp):
        """Dump body."""
        resp.body = ujson.dumps(self.body)
        resp.status = falcon.HTTP_200
