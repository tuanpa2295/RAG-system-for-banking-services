#!/usr/bin/env python3
"""
Banking RAG Server

Flask web server that provides REST API endpoints for the Banking RAG system.
Accepts queries and returns AI-generated responses based on banking knowledge.

Endpoints:
- POST /api/v1/query - Submit a banking question
- GET /api/v1/health - Check service health
- GET /api/v1/categories - Get available document categories
- POST /api/v1/batch - Process multiple queries

Author: GitHub Copilot
Date: August 2, 2025
"""

import os
import json
from datetime import datetime
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from rag_service import BankingRAGService

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration

# Initialize RAG service
rag_service = BankingRAGService()

# HTML template for the web interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Banking RAG System</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f8f9fa;
        }
        .header {
            text-align: center;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
        }
        .container {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin-bottom: 30px;
        }
        .query-panel, .response-panel {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .query-input {
            width: 100%;
            padding: 15px;
            border: 2px solid #e1e5e9;
            border-radius: 8px;
            font-size: 16px;
            margin-bottom: 15px;
            min-height: 100px;
            resize: vertical;
        }
        .query-button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 30px;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
            transition: all 0.3s;
        }
        .query-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }
        .query-button:disabled {
            background: #ccc;
            cursor: not-allowed;
            transform: none;
        }
        .response-area {
            min-height: 200px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 8px;
            white-space: pre-wrap;
            font-family: 'Georgia', serif;
            line-height: 1.6;
        }
        .sources {
            margin-top: 20px;
            padding: 15px;
            background: #e8f4fd;
            border-left: 4px solid #007bff;
            border-radius: 0 8px 8px 0;
        }
        .source-item {
            margin: 5px 0;
            font-size: 14px;
        }
        .sample-queries {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .sample-button {
            background: #f8f9fa;
            border: 1px solid #dee2e6;
            padding: 10px 15px;
            margin: 5px;
            border-radius: 5px;
            cursor: pointer;
            display: inline-block;
            font-size: 14px;
            transition: all 0.2s;
        }
        .sample-button:hover {
            background: #e9ecef;
            border-color: #adb5bd;
        }
        .loading {
            color: #666;
            font-style: italic;
        }
        .confidence {
            float: right;
            background: #28a745;
            color: white;
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 12px;
        }
        .confidence.medium { background: #ffc107; color: #212529; }
        .confidence.low { background: #dc3545; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🏦 Banking RAG System</h1>
        <p>AI-Powered Banking & Financial Services Q&A</p>
    </div>

    <div class="container">
        <div class="query-panel">
            <h3>Ask a Banking Question</h3>
            <textarea id="queryInput" class="query-input" placeholder="Type your banking question here, for example: 'What are the requirements for getting a personal loan?'"></textarea>
            <button id="submitBtn" class="query-button" onclick="submitQuery()">Submit Query</button>
        </div>

        <div class="response-panel">
            <h3>AI Response</h3>
            <div id="responseArea" class="response-area">
                Welcome to the Banking RAG System! Ask any banking or financial services question and get instant, accurate answers based on our comprehensive knowledge base.
            </div>
            <div id="sourcesArea" class="sources" style="display: none;">
                <strong>Sources:</strong>
                <div id="sourcesList"></div>
            </div>
        </div>
    </div>

    <div class="sample-queries">
        <h3>Sample Questions</h3>
        <p>Click any sample question to try it out:</p>
        <div class="sample-button" onclick="setQuery('What are the requirements for getting a personal loan?')">Personal Loan Requirements</div>
        <div class="sample-button" onclick="setQuery('How do I open a savings account and what are the benefits?')">Savings Account Information</div>
        <div class="sample-button" onclick="setQuery('What is the process for applying for a credit card?')">Credit Card Application</div>
        <div class="sample-button" onclick="setQuery('What investment options do you offer?')">Investment Options</div>
        <div class="sample-button" onclick="setQuery('How secure is mobile banking?')">Mobile Banking Security</div>
        <div class="sample-button" onclick="setQuery('What do I need to qualify for a mortgage?')">Mortgage Requirements</div>
        <div class="sample-button" onclick="setQuery('What business banking services are available?')">Business Banking</div>
        <div class="sample-button" onclick="setQuery('What are the current interest rates?')">Interest Rates</div>
    </div>

    <script>
        function setQuery(query) {
            document.getElementById('queryInput').value = query;
        }

        async function submitQuery() {
            const query = document.getElementById('queryInput').value.trim();
            const submitBtn = document.getElementById('submitBtn');
            const responseArea = document.getElementById('responseArea');
            const sourcesArea = document.getElementById('sourcesArea');
            const sourcesList = document.getElementById('sourcesList');

            if (!query) {
                alert('Please enter a question');
                return;
            }

            // Disable button and show loading
            submitBtn.disabled = true;
            submitBtn.textContent = 'Processing...';
            responseArea.innerHTML = 'Processing your question...';
            responseArea.className = 'response-area loading';
            sourcesArea.style.display = 'none';

            try {
                const response = await fetch('/api/v1/query', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ query: query })
                });

                const data = await response.json();

                if (data.status === 'success') {
                    responseArea.innerHTML = data.answer;
                    responseArea.className = 'response-area';

                    // Show sources
                    if (data.sources && data.sources.length > 0) {
                        sourcesList.innerHTML = '';
                        data.sources.forEach(source => {
                            const sourceItem = document.createElement('div');
                            sourceItem.className = 'source-item';
                            const confidenceClass = source.relevance_score > 0.8 ? 'high' : source.relevance_score > 0.6 ? 'medium' : 'low';
                            sourceItem.innerHTML = `
                                <strong>${source.title}</strong> (${source.category})
                                <span class="confidence ${confidenceClass}">${(source.relevance_score * 100).toFixed(0)}%</span>
                            `;
                            sourcesList.appendChild(sourceItem);
                        });
                        sourcesArea.style.display = 'block';
                    }
                } else {
                    responseArea.innerHTML = 'Error: ' + (data.message || 'Unknown error occurred');
                    responseArea.className = 'response-area';
                }
            } catch (error) {
                responseArea.innerHTML = 'Error: Unable to process request. Please try again.';
                responseArea.className = 'response-area';
                console.error('Error:', error);
            } finally {
                // Re-enable button
                submitBtn.disabled = false;
                submitBtn.textContent = 'Submit Query';
            }
        }

        // Allow Enter key to submit
        document.getElementById('queryInput').addEventListener('keydown', function(event) {
            if (event.key === 'Enter' && !event.shiftKey) {
                event.preventDefault();
                submitQuery();
            }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Serve the web interface."""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/v1/health', methods=['GET'])
def health_check():
    """Check service health status."""
    try:
        status = rag_service.get_health_status()
        return jsonify({
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "service_info": status
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@app.route('/api/v1/query', methods=['POST'])
def process_query():
    """Process a banking question and return AI-generated response."""
    try:
        # Get request data
        data = request.get_json()
        
        if not data or 'query' not in data:
            return jsonify({
                "status": "error",
                "message": "Missing 'query' field in request body"
            }), 400
        
        query = data['query'].strip()
        
        if not query:
            return jsonify({
                "status": "error", 
                "message": "Query cannot be empty"
            }), 400
        
        # Process the query
        result = rag_service.answer_question(query)
        
        # Add timestamp
        result['timestamp'] = datetime.now().isoformat()
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@app.route('/api/v1/categories', methods=['GET'])
def get_categories():
    """Get available document categories."""
    try:
        if not rag_service.is_initialized:
            rag_service.initialize()
        
        categories = {}
        for doc in rag_service.documents:
            if doc.category not in categories:
                categories[doc.category] = []
            categories[doc.category].append({
                "id": doc.id,
                "title": doc.title,
                "source": doc.source
            })
        
        return jsonify({
            "status": "success",
            "categories": categories,
            "total_documents": len(rag_service.documents),
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@app.route('/api/v1/batch', methods=['POST'])
def process_batch_queries():
    """Process multiple queries in batch."""
    try:
        data = request.get_json()
        
        if not data or 'queries' not in data:
            return jsonify({
                "status": "error",
                "message": "Missing 'queries' field in request body"
            }), 400
        
        queries = data['queries']
        
        if not isinstance(queries, list) or len(queries) == 0:
            return jsonify({
                "status": "error",
                "message": "Queries must be a non-empty list"
            }), 400
        
        if len(queries) > 10:  # Limit batch size
            return jsonify({
                "status": "error", 
                "message": "Maximum 10 queries per batch"
            }), 400
        
        # Process all queries
        results = []
        for i, query in enumerate(queries):
            if isinstance(query, str) and query.strip():
                result = rag_service.answer_question(query.strip())
                result['batch_index'] = i
                results.append(result)
            else:
                results.append({
                    "batch_index": i,
                    "status": "error",
                    "message": "Invalid query format"
                })
        
        return jsonify({
            "status": "success",
            "results": results,
            "batch_size": len(queries),
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@app.route('/api/v1/documents', methods=['GET', 'POST'])
def manage_documents():
    """Manage documents in the knowledge base."""
    if request.method == 'GET':
        try:
            documents = rag_service.list_documents()
            
            return jsonify({
                "status": "success",
                "documents": documents,
                "total_documents": len(documents),
                "timestamp": datetime.now().isoformat()
            })
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": str(e),
                "timestamp": datetime.now().isoformat()
            }), 500
    
    elif request.method == 'POST':
        """Add a new document to the knowledge base."""
        try:
            data = request.get_json()
            
            required_fields = ['id', 'title', 'content', 'category', 'source']
            for field in required_fields:
                if field not in data:
                    return jsonify({
                        "status": "error",
                        "message": f"Missing required field: {field}"
                    }), 400
            
            # Create new document
            from models import BankingDocument
            new_doc = BankingDocument(
                id=data['id'],
                title=data['title'],
                content=data['content'],
                category=data['category'],
                source=data['source']
            )
            
            # Add to RAG service
            success = rag_service.add_document(new_doc)
            
            if success:
                return jsonify({
                    "status": "success",
                    "message": "Document added successfully",
                    "document_id": new_doc.id,
                    "total_documents": len(rag_service.documents),
                    "timestamp": datetime.now().isoformat()
                })
            else:
                return jsonify({
                    "status": "error",
                    "message": "Failed to add document",
                    "timestamp": datetime.now().isoformat()
                }), 500
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": str(e),
                "timestamp": datetime.now().isoformat()
            }), 500

@app.route('/api/v1/documents/<doc_id>', methods=['DELETE'])
def delete_document(doc_id):
    """Delete a document from the knowledge base."""
    try:
        success = rag_service.remove_document(doc_id)
        
        if success:
            return jsonify({
                "status": "success",
                "message": f"Document {doc_id} deleted successfully",
                "total_documents": len(rag_service.documents),
                "timestamp": datetime.now().isoformat()
            })
        else:
            return jsonify({
                "status": "error",
                "message": f"Document {doc_id} not found",
                "timestamp": datetime.now().isoformat()
            }), 404
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@app.route('/api/v1/reindex', methods=['POST'])
def reindex_documents():
    """Rebuild the vector index with current documents."""
    try:
        rag_service.rebuild_index()
        
        return jsonify({
            "status": "success",
            "message": "Vector index rebuilt successfully",
            "total_documents": len(rag_service.documents),
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        "status": "error",
        "message": "Endpoint not found",
        "timestamp": datetime.now().isoformat()
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({
        "status": "error",
        "message": "Internal server error",
        "timestamp": datetime.now().isoformat()
    }), 500

def initialize_service():
    """Initialize the RAG service on startup."""
    print("="*60)
    print("🏦 BANKING RAG SERVER STARTING UP")
    print("="*60)
    
    try:
        rag_service.initialize()
        print("✅ RAG Service initialized successfully")
    except Exception as e:
        print(f"❌ Error initializing RAG service: {str(e)}")
        print("⚠️  Server will start but may have limited functionality")
    
    print("="*60)
    print("🚀 Server ready to accept requests")
    print("📱 Web interface: http://localhost:5000")
    print("🔗 API endpoint: http://localhost:5000/api/v1/query")
    print("🏥 Health check: http://localhost:5000/api/v1/health")
    print("="*60)

if __name__ == '__main__':
    # Initialize service on startup
    initialize_service()
    
    # Start the Flask server
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        threaded=True
    )
