#!/usr/bin/env python3
"""
Quick Start Script for Banking RAG System

This script provides a simple way to start the Banking RAG system
with proper environment setup and initialization.
"""

import os
import sys
from pathlib import Path

def check_environment():
    """Check if environment is properly configured."""
    print("🔍 Checking environment configuration...")
    
    # Change to the script's directory
    script_dir = Path(__file__).parent.absolute()
    os.chdir(script_dir)
    
    env_file = Path("config/.env")
    if not env_file.exists():
        print("❌ Environment file not found at config/.env")
        print("   Please copy config/.env.example to config/.env and configure it")
        return False
    
    # Check for required environment variables
    from dotenv import load_dotenv
    load_dotenv(env_file)
    
    required_vars = [
        "AZURE_OPENAI_API_KEY",
        "AZURE_OPENAI_ENDPOINT"
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        return False
    
    print("✅ Environment configuration looks good")
    return True

def check_dependencies():
    """Check if required dependencies are installed."""
    print("📦 Checking dependencies...")
    
    required_packages = [
        "flask",
        "flask_cors", 
        "openai",
        "faiss",
        "numpy",
        "dotenv"
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing required packages: {', '.join(missing_packages)}")
        print("   Please run: pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies are installed")
    return True

def main():
    """Main startup function."""
    print("="*60)
    print("🏦 BANKING RAG SYSTEM - QUICK START")
    print("="*60)
    
    # Check environment and dependencies
    if not check_environment():
        sys.exit(1)
    
    if not check_dependencies():
        sys.exit(1)
    
    print("\n🚀 Starting Banking RAG System...")
    print("   This may take a few moments to initialize...")
    
    # Import and run the main application
    try:
        from main import main as app_main
        app_main()
    except KeyboardInterrupt:
        print("\n\n👋 Banking RAG System stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting application: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
