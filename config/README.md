# Configuration package for the Banking RAG System
#
# This directory contains all configuration files:
# - .env: Environment variables (API keys, endpoints)
# - settings.py: Application settings and constants

# Environment Variables Template
# Copy this to .env and fill in your actual values

# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY=your_api_key_here
AZURE_OPENAI_ENDPOINT=https://your-endpoint.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME=text-embedding-3-small
AZURE_OPENAI_API_VERSION=2024-02-01

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=true
FLASK_PORT=5000

# RAG Configuration
MAX_DOCUMENTS_PER_QUERY=3
EMBEDDING_DIMENSION=1536
VECTOR_INDEX_TYPE=cosine
