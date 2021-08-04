"""Document Text Extractor.

Bjoern runner
"""
import bjoern
try:
    from .src.textractor import create_app
except ImportError:
    from src.textractor import create_app

# Define webserver host and port
WEB_HOST = '0.0.0.0'
PORT = 8060

# Run the app
if __name__ == "__main__":
    app = create_app()
    bjoern.run(app, WEB_HOST, PORT)
