#!/usr/bin/env python3
"""
Banking RAG Server Startup Script

Simple script to start the Banking RAG server with proper configuration.
Handles environment setup and provides clear startup information.

Usage:
    python start_server.py
    python start_server.py --port 8080
    python start_server.py --host 0.0.0.0 --port 5000
"""

import argparse
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_dependencies():
    """Check if required dependencies are installed."""
    required_packages = [
        ('flask', 'Flask'),
        ('openai', 'OpenAI'),
        ('numpy', 'NumPy'),
    ]
    
    missing_packages = []
    
    for package_name, display_name in required_packages:
        try:
            __import__(package_name)
        except ImportError:
            missing_packages.append(display_name)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n💡 Install dependencies with:")
        print("   pip install -r requirements.txt")
        return False
    
    return True

def setup_environment():
    """Set up environment variables."""
    # Set default Azure OpenAI configuration if not provided
    if not os.getenv("AZURE_OPENAI_API_KEY"):
        print("⚠️  AZURE_OPENAI_API_KEY not found in environment")
        print("   Server will use mock responses for demonstration")
    
    if not os.getenv("AZURE_OPENAI_ENDPOINT"):
        print("⚠️  AZURE_OPENAI_ENDPOINT not found in environment")
        print("   Server will use mock responses for demonstration")
    
    # Add current directory to Python path
    current_dir = Path(__file__).parent
    if str(current_dir) not in sys.path:
        sys.path.insert(0, str(current_dir))

def main():
    """Main startup function."""
    parser = argparse.ArgumentParser(description='Start the Banking RAG Server')
    parser.add_argument('--host', default='0.0.0.0', help='Host address (default: 0.0.0.0)')
    parser.add_argument('--port', type=int, default=5000, help='Port number (default: 5000)')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    args = parser.parse_args()

    print("🏦 Banking RAG Server Startup")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        return 1
    
    # Setup environment
    setup_environment()
    
    # Import and start server
    try:
        from server import app, initialize_service
        
        # Initialize the RAG service
        initialize_service()
        
        # Start the Flask server
        print(f"🚀 Starting server on http://{args.host}:{args.port}")
        
        app.run(
            host=args.host,
            port=args.port,
            debug=args.debug,
            threaded=True
        )
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Make sure all required files are in the current directory")
        return 1
    except Exception as e:
        print(f"❌ Server error: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
