#!/usr/bin/env python3
"""
Banking RAG System - Main Application Entry Point

This is the main entry point for the Banking RAG System.
It initializes and starts the Flask web server with all components.

Usage:
    python main.py

Author: Banking RAG Team
Date: August 2, 2025
"""

import os
import sys
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from api.server import create_app
from core.rag_service import BankingRAGService

def main():
    """Main application entry point."""
    print("="*60)
    print("🏦 BANKING RAG SYSTEM STARTING UP")
    print("="*60)
    
    # Initialize RAG service
    rag_service = BankingRAGService()
    
    try:
        rag_service.initialize()
        print("✅ RAG Service initialized successfully")
    except Exception as e:
        print(f"❌ Error initializing RAG service: {str(e)}")
        print("⚠️  Server will start but may have limited functionality")
    
    # Create Flask app
    app = create_app(rag_service)
    
    print("="*60)
    print("🚀 Server ready to accept requests")
    print("📱 Web interface: http://localhost:5001")
    print("🔗 API endpoint: http://localhost:5001/api/v1/query")
    print("🏥 Health check: http://localhost:5001/api/v1/health")
    print("="*60)
    
    # Start the Flask server
    app.run(
        host='0.0.0.0',
        port=5001,
        debug=True,
        threaded=True
    )

if __name__ == '__main__':
    main()
