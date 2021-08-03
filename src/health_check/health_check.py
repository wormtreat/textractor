"""Document Text Extractor.

HealthCheck class
"""


class HealthCheck():
    """Healthcheck for container service."""

    def __init__(self, body):
        self.set_body(body)

    def set_body(self, body):
        """"Set document body."""
        self.body = body

    def get_body(self):
        """"Get document body."""
        return self.body
