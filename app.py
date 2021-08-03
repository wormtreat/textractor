"""Document Text Extractor.

Bjoern runner
"""
# Run the app
import bjoern
from src.textractor import create_app

# Define webserver host and port
WEB_HOST = '0.0.0.0'
PORT = 8060

if __name__ == "__main__":
    app = create_app()
    bjoern.run(app, WEB_HOST, PORT)
