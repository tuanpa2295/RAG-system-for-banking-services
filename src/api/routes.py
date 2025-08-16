"""
API Routes for Banking RAG System

Flask Blueprint containing all API endpoints for the Banking RAG system.
"""

from datetime import datetime
import time
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from core.rag_service import BankingRAGService
from models import BankingDocument

# Create blueprint
api_blueprint = Blueprint('api', __name__, url_prefix='/api/v1')

@api_blueprint.route('/add-qsa', methods=['GET', 'POST'])
def add_qsa():
    """Handle adding new Q&A documents through web interface."""
    if request.method == 'POST':
        try:
            # Get form data
            question = request.form.get('question')
            answer = request.form.get('answer')
            category = request.form.get('category')
            source = request.form.get('source', 'Web Interface')
            
            if not all([question, answer, category]):
                flash('Please fill in all required fields', 'error')
                return redirect(url_for('api.add_qsa'))

            # Create new document
            new_doc = BankingDocument(
                id=f'doc_{int(time.time())}',
                title=question[:50] + '...',
                content=f'Q: {question}\nA: {answer}',
                category=category,
                source=source,
                date_added=datetime.now().isoformat()
            )

            # Add to knowledge base
            rag_service.add_document(new_doc)
            
            # Trigger reindex
            rag_service.reindex()

            flash('Document added successfully!', 'success')
            return redirect(url_for('api.add_qsa'))

        except Exception as e:
            flash(f'Error adding document: {str(e)}', 'error')
            return redirect(url_for('api.add_qsa'))

    # GET request - show form
    categories = [
        'Personal Loans',
        'Savings & Checking',
        'Credit Cards',
        'Investments',
        'Mobile Banking',
        'Mortgages',
        'Business Banking',
        'Regulations',
        'Customer Support',
        'Digital Assets',
        'Wealth Management'
    ]
    
    return render_template('add_qsa.html', categories=categories)

# Global RAG service instance (will be set by the main app)
rag_service: BankingRAGService = None

def set_rag_service(service: BankingRAGService):
    """Set the RAG service instance for the API routes."""
    global rag_service
    rag_service = service

@api_blueprint.route('/health', methods=['GET'])
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

@api_blueprint.route('/query', methods=['POST'])
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

@api_blueprint.route('/categories', methods=['GET'])
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

@api_blueprint.route('/batch', methods=['POST'])
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

@api_blueprint.route('/documents', methods=['GET', 'POST'])
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

@api_blueprint.route('/documents/<doc_id>', methods=['DELETE'])
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

@api_blueprint.route('/reindex', methods=['POST'])
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
