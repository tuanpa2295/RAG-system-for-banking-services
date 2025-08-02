# Banking RAG Server

A Flask-based REST API server that provides AI-powered banking and financial services Q&A using Retrieval-Augmented Generation (RAG) with Azure OpenAI.

## 🏗️ Architecture

The server is built with a modular architecture:

```
project01/
├── server.py              # Flask web server with REST API
├── rag_service.py         # Core RAG service functionality  
├── models.py              # Data models and knowledge base
├── start_server.py        # Startup script
├── requirements.txt       # Python dependencies
└── README_SERVER.md       # This documentation
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables (Optional)

For full functionality with Azure OpenAI:

```bash
export AZURE_OPENAI_API_KEY="your-api-key"
export AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/"
export AZURE_OPENAI_DEPLOYMENT_NAME="gpt-4o-mini"
export AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME="text-embedding-ada-002"
export AZURE_OPENAI_API_VERSION="2024-02-01"
```

**Note:** The server will work without these variables by using mock responses for demonstration.

### 3. Start the Server

```bash
# Simple start
python start_server.py

# Custom host and port
python start_server.py --host 0.0.0.0 --port 8080

# With debug mode
python start_server.py --debug
```

## 🌐 API Endpoints

### Web Interface
- **GET** `/` - Interactive web interface for testing queries

### REST API

#### Query Processing
- **POST** `/api/v1/query`
  ```json
  {
    "query": "What are the requirements for getting a personal loan?"
  }
  ```
  
  Response:
  ```json
  {
    "status": "success",
    "query": "What are the requirements for getting a personal loan?",
    "answer": "To qualify for a personal loan, you typically need...",
    "sources": [
      {
        "id": "loan_001",
        "title": "Personal Loan Requirements",
        "category": "Loans",
        "relevance_score": 0.95
      }
    ],
    "timestamp": "2025-01-02T10:30:00.123456"
  }
  ```

#### Health Check
- **GET** `/api/v1/health`
  ```json
  {
    "status": "success",
    "service_info": {
      "rag_initialized": true,
      "documents_loaded": 10,
      "vector_index_ready": true,
      "azure_openai_available": true
    },
    "timestamp": "2025-01-02T10:30:00.123456"
  }
  ```

#### Categories
- **GET** `/api/v1/categories`
  ```json
  {
    "status": "success",
    "categories": {
      "Loans": [
        {"id": "loan_001", "title": "Personal Loan Requirements", "source": "Bank Policy"},
        {"id": "loan_002", "title": "Mortgage Application Process", "source": "Lending Guide"}
      ],
      "Accounts": [
        {"id": "acc_001", "title": "Savings Account Benefits", "source": "Product Guide"}
      ]
    },
    "total_documents": 10
  }
  ```

#### Batch Processing
- **POST** `/api/v1/batch`
  ```json
  {
    "queries": [
      "What are the current interest rates?",
      "How do I open a savings account?",
      "What investment options are available?"
    ]
  }
  ```

## 🧪 Testing the Server

### Using curl

```bash
# Health check
curl http://localhost:5000/api/v1/health

# Submit a query
curl -X POST http://localhost:5000/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the requirements for getting a personal loan?"}'

# Get categories
curl http://localhost:5000/api/v1/categories

# Batch queries
curl -X POST http://localhost:5000/api/v1/batch \
  -H "Content-Type: application/json" \
  -d '{"queries": ["What are current rates?", "How to open account?"]}'
```

### Using Python

```python
import requests

# Submit a query
response = requests.post('http://localhost:5000/api/v1/query', 
    json={'query': 'What are the requirements for getting a personal loan?'})
print(response.json())

# Check health
health = requests.get('http://localhost:5000/api/v1/health')
print(health.json())
```

### Using the Web Interface

1. Open http://localhost:5000 in your browser
2. Type your banking question in the text area
3. Click "Submit Query" or press Enter
4. View the AI-generated response and sources

## 📊 Knowledge Base

The system includes comprehensive banking knowledge across 9 categories:

- **Loans** - Personal loans, mortgages, requirements
- **Accounts** - Savings, checking, account management  
- **Credit** - Credit cards, credit scores, applications
- **Investments** - Investment options, financial planning
- **Security** - Banking security, fraud protection
- **Business** - Business banking services
- **Regulations** - Banking regulations, compliance
- **Interest Rates** - Current rates, rate information
- **Customer Support** - Support services, contact information

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `AZURE_OPENAI_API_KEY` | Azure OpenAI API key | None (uses mock) |
| `AZURE_OPENAI_ENDPOINT` | Azure OpenAI endpoint URL | None (uses mock) |
| `AZURE_OPENAI_DEPLOYMENT_NAME` | GPT model deployment name | "gpt-4o-mini" |
| `AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME` | Embedding model deployment | "text-embedding-ada-002" |
| `AZURE_OPENAI_API_VERSION` | API version | "2024-02-01" |

### Server Configuration

```python
# In server.py, modify these settings:
app.run(
    host='0.0.0.0',    # Listen on all interfaces
    port=5000,         # Server port
    debug=True,        # Debug mode
    threaded=True      # Enable threading
)
```

## 🐳 Docker Deployment

### Quick Start with Docker Compose

1. **Copy environment template**:
   ```bash
   cp .env.example .env
   # Edit .env with your Azure OpenAI credentials
   ```

2. **Start with Docker Compose**:
   ```bash
   docker-compose up -d
   ```

3. **Check status**:
   ```bash
   docker-compose ps
   docker-compose logs banking-rag-server
   ```

4. **Access the application**:
   - Web Interface: http://localhost:5000
   - API: http://localhost:5000/api/v1/query

### Manual Docker Build

1. **Build the image**:
   ```bash
   docker build -t banking-rag-server .
   ```

2. **Run the container**:
   ```bash
   docker run -d \
     --name banking-rag-server \
     -p 5000:5000 \
     -e AZURE_OPENAI_API_KEY="your-key" \
     -e AZURE_OPENAI_ENDPOINT="your-endpoint" \
     banking-rag-server
   ```

3. **View logs**:
   ```bash
   docker logs -f banking-rag-server
   ```

### Docker Features

- **Multi-stage build** for optimized image size
- **Non-root user** for security
- **Health checks** for container monitoring
- **Volume persistence** for data and logs
- **Resource limits** for production deployment
- **Automatic restart** on failure

### Production Deployment

For production deployment, consider:

```bash
# Use specific version tags
docker build -t banking-rag-server:v1.0.0 .

# Run with resource limits
docker run -d \
  --name banking-rag-server \
  --memory="1g" \
  --cpus="0.5" \
  --restart=unless-stopped \
  -p 5000:5000 \
  banking-rag-server:v1.0.0
```

## 🔍 Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   pip install -r requirements.txt
   ```

2. **FAISS Issues on M1 Mac**
   ```bash
   pip install faiss-cpu --no-cache-dir
   ```

3. **Port Already in Use**
   ```bash
   python start_server.py --port 8080
   ```

4. **Azure OpenAI Not Available**
   - Server automatically falls back to mock responses
   - Check environment variables
   - Verify API key and endpoint

### Debugging

Enable debug mode for detailed error information:

```bash
python start_server.py --debug
```

Check the health endpoint for system status:

```bash
curl http://localhost:5000/api/v1/health
```

## 📈 Performance

- **Response Time**: Typically 1-3 seconds per query
- **Concurrent Users**: Supports multiple concurrent requests
- **Memory Usage**: ~200-500MB depending on vector index size
- **Throughput**: ~10-50 requests per second

## 🔐 Security Considerations

- API key should be kept secure in environment variables
- Consider adding authentication for production use
- Rate limiting may be needed for public deployment
- CORS is enabled for frontend integration

## 🎯 Use Cases

- **Customer Service**: Automated banking FAQ responses
- **Employee Training**: Internal knowledge base for staff
- **Documentation**: Searchable banking policy information
- **Chatbot Backend**: AI-powered customer support
- **API Integration**: Embed banking Q&A in other applications

## 📝 License

This project is for educational and demonstration purposes.
