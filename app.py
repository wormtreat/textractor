"""Document Text Extractor.

Bjoern runner
"""
# Run the app
import bjoern
from textractor import Textractor

# Define webserver host and port
WEB_HOST = '0.0.0.0'
PORT = 8060

app = Textractor.create_app()

bjoern.run(app, WEB_HOST, PORT)
