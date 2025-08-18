"""
Flask Server for Banking RAG System

Main Flask application factory and server configuration.
"""

from datetime import datetime
import os
from flask import Flask, render_template, render_template_string
from flask_cors import CORS

from .routes import api_blueprint, set_rag_service, set_chat_service
from web.templates import HTML_TEMPLATE
from core.rag_service import BankingRAGService
from models.database import init_db
from models.chat_service import ChatService

def create_app(rag_service: BankingRAGService) -> Flask:
    """
    Create and configure the Flask application.
    
    Args:
        rag_service: Initialized RAG service instance
        
    Returns:
        Configured Flask application
    """
    # Initialize Flask app with template folder
    app = Flask(__name__,
                template_folder=os.path.join(os.path.dirname(__file__), '../web/templates'))
    
    # Set secret key for session and flash messages
    app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'dev-secret-key-123')  # In production, use proper secret key
    
    CORS(app)  # Enable CORS for frontend integration
    
    # Initialize database
    try:
        init_db(app)
        print("✅ Database initialized successfully")
        
        # Initialize chat service
        chat_service = ChatService()
        set_chat_service(chat_service)
        print("✅ Chat service initialized successfully")
        
    except Exception as e:
        print(f"⚠️  Warning: Chat service not available - {str(e)}")
        set_chat_service(None)
    
    # Set RAG service for API routes
    set_rag_service(rag_service)
    
    # Register blueprints
    app.register_blueprint(api_blueprint)
    
    # Main web interface route
    @app.route('/')
    def index():
        """Serve the web interface."""
        return render_template_string(HTML_TEMPLATE)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors."""
        return {
            "status": "error",
            "message": "Endpoint not found",
            "timestamp": datetime.now().isoformat()
        }, 404

    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors."""
        return {
            "status": "error",
            "message": "Internal server error",
            "timestamp": datetime.now().isoformat()
        }, 500
    
    return app
