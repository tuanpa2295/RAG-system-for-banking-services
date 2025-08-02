# Banking RAG System

A comprehensive Retrieval-Augmented Generation (RAG) system for banking and financial services Q&A, built with Flask, Azure OpenAI, and FAISS vector search.

## 🏗️ Architecture Overview

```
project01/
├── main.py                 # Application entry point
├── src/                    # Source code
│   ├── api/               # Flask API and routes
│   │   ├── __init__.py
│   │   ├── server.py      # Flask app factory
│   │   └── routes.py      # API endpoints
│   ├── core/              # Core business logic
│   │   ├── __init__.py
│   │   └── rag_service.py # RAG implementation
│   ├── models/            # Data models and knowledge base
│   │   ├── __init__.py
│   │   ├── banking_models.py  # Data structures
│   │   └── knowledge_base.py  # Banking documents
│   └── web/               # Web interface
│       ├── __init__.py
│       └── templates.py   # HTML templates
├── config/                # Configuration files
│   ├── .env              # Environment variables
│   └── README.md         # Config documentation
├── data/                  # Data storage
│   ├── *.faiss           # Vector indexes
│   └── *.pkl             # Document metadata
├── docs/                  # Documentation
├── archive/              # Legacy files
└── requirements.txt      # Python dependencies
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Azure OpenAI API access
- Required Python packages (see requirements.txt)

### Installation

1. **Clone and navigate to the project:**
   ```bash
   cd /Users/anhtuanpham/projects/fsoft-assignments/project01
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   ```bash
   cp config/.env.example config/.env
   # Edit config/.env with your Azure OpenAI credentials
   ```

4. **Run the application:**
   ```bash
   python main.py
   ```

5. **Access the system:**
   - Web Interface: http://localhost:5000
   - API Documentation: http://localhost:5000/api/v1/health
   - Health Check: http://localhost:5000/api/v1/health

## 🔧 Configuration

### Environment Variables

Create a `config/.env` file with:

```env
# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY=your_api_key_here
AZURE_OPENAI_ENDPOINT=https://your-endpoint.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME=text-embedding-3-small
AZURE_OPENAI_API_VERSION=2024-02-01

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=true
```

## 📚 Knowledge Base

The system includes comprehensive banking knowledge covering:

- **Personal Loans**: Requirements, application process, rates
- **Savings & Checking**: Account features, benefits, requirements
- **Credit Cards**: Application process, approval criteria
- **Investments**: IRA, 401k, brokerage accounts, mutual funds
- **Mobile Banking**: Security features, digital services
- **Mortgages**: Loan process, requirements, rates
- **Business Banking**: Commercial services, SBA loans
- **Regulations**: Federal banking compliance, privacy
- **Customer Support**: Service channels, response times
- **Digital Assets**: Cryptocurrency services
- **Wealth Management**: Private banking, portfolio management

## 🌐 API Endpoints

### Core Endpoints

- `POST /api/v1/query` - Submit banking questions
- `GET /api/v1/health` - Service health status
- `GET /api/v1/categories` - Available document categories
- `POST /api/v1/batch` - Process multiple queries

### Document Management

- `GET /api/v1/documents` - List all documents
- `POST /api/v1/documents` - Add new document
- `DELETE /api/v1/documents/<id>` - Remove document
- `POST /api/v1/reindex` - Rebuild vector index

### Example API Usage

```bash
# Ask a question
curl -X POST http://localhost:5000/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the requirements for a personal loan?"}'

# Check health
curl http://localhost:5000/api/v1/health
```

## 🎯 Features

### Intelligent Q&A System
- **Semantic Search**: FAISS-powered vector similarity search
- **AI Responses**: GPT-4 powered natural language generation
- **Context-Aware**: Retrieves relevant documents before generating responses
- **Multi-Document**: Combines information from multiple sources

### Web Interface
- **Modern UI**: Clean, responsive design
- **Real-time**: Instant query processing
- **Source Attribution**: Shows confidence scores and sources
- **Sample Queries**: Pre-built questions for testing

### Document Management
- **Dynamic Updates**: Add/remove documents without restart
- **Vector Indexing**: Automatic embedding generation
- **Categorization**: Organized by banking service type
- **Metadata Tracking**: Source attribution and relevance scoring

### Production Ready
- **Error Handling**: Comprehensive error management
- **Logging**: Detailed operation logging
- **Health Monitoring**: Service status endpoints
- **Scalable Architecture**: Modular, maintainable codebase

## 🔍 How It Works

1. **Document Ingestion**: Banking documents are embedded using Azure OpenAI
2. **Vector Storage**: Embeddings stored in FAISS index for fast retrieval  
3. **Query Processing**: User questions are embedded and matched against documents
4. **Context Retrieval**: Most relevant documents are retrieved based on similarity
5. **Response Generation**: GPT-4 generates responses using retrieved context
6. **Source Attribution**: Results include confidence scores and source documents

## 🛠️ Development

### Project Structure

- **`src/api/`**: Flask application and REST API endpoints
- **`src/core/`**: RAG service implementation and business logic
- **`src/models/`**: Data models and banking knowledge base
- **`src/web/`**: Web interface templates and static assets
- **`config/`**: Configuration files and environment variables
- **`data/`**: Vector indexes and document storage
- **`docs/`**: Comprehensive documentation

### Code Organization

The codebase follows a clean architecture pattern:
- **Separation of Concerns**: API, business logic, and data layers
- **Dependency Injection**: Services passed through application factory
- **Error Handling**: Consistent error responses across all endpoints
- **Type Hints**: Full type annotations for better code quality

### Testing

Test the system with sample queries:
- Personal loan requirements
- Savings account benefits  
- Credit card applications
- Investment options
- Mobile banking security
- Mortgage processes
- Business banking services

## 📈 Performance

- **Fast Retrieval**: FAISS vector search in milliseconds
- **Concurrent Requests**: Multi-threaded Flask server
- **Caching**: Vector indexes cached for repeated queries
- **Batch Processing**: Support for multiple queries in single request

## 🔒 Security

- **API Key Management**: Secure environment variable storage
- **Input Validation**: Comprehensive request validation
- **Error Masking**: Detailed errors only in development mode
- **CORS Support**: Configurable cross-origin resource sharing

## 📊 Monitoring

- **Health Endpoints**: Real-time service status
- **Document Metrics**: Track knowledge base size and categories
- **Query Analytics**: Monitor popular questions and response quality
- **Error Tracking**: Comprehensive error logging and reporting

## 🚀 Deployment

1. **Set Environment Variables**: Configure Azure OpenAI credentials
2. **Install Dependencies**: `pip install -r requirements.txt`
3. **Initialize Service**: Run `python main.py`
4. **Monitor Health**: Check `/api/v1/health` endpoint
5. **Scale as Needed**: Add load balancing for high traffic

## 📝 License

This project is part of the FSoft assignments and is intended for educational and demonstration purposes.

## 🤝 Contributing

1. Follow the established code structure
2. Add comprehensive docstrings
3. Include error handling
4. Update documentation as needed
5. Test all endpoints before committing

---

*Built with ❤️ for comprehensive banking Q&A experiences*
