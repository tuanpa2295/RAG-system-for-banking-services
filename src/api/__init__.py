"""
API package for the Banking RAG System.

This package contains Flask routes and API endpoints.
"""

from .server import create_app
from .routes import api_blueprint

__all__ = ['create_app', 'api_blueprint']
