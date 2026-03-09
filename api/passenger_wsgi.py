import sys
import os

# Add application directory to path
sys.path.insert(0, os.path.dirname(__file__))

from a2wsgi import ASGIMiddleware
from main import app

# Passenger requires 'application' as WSGI callable
# a2wsgi wraps the ASGI app (FastAPI) for WSGI compatibility
application = ASGIMiddleware(app)
