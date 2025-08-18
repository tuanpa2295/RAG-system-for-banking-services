"""
API Routes for Banking RAG System

Flask Blueprint containing all API endpoints for the Banking RAG system.
"""

from datetime import datetime
import time
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from core.rag_service import BankingRAGService
from models import BankingDocument
from models.chat_service import ChatService

# Create blueprint
api_blueprint = Blueprint('api', __name__, url_prefix='/api/v1')

# Global service instances (will be set by the main app)
rag_service: BankingRAGService = None
chat_service: ChatService = None

def set_rag_service(service: BankingRAGService):
    """Set the global RAG service instance."""
    global rag_service
    rag_service = service

def set_chat_service(service: ChatService):
    """Set the global chat service instance."""
    global chat_service
    chat_service = service

def set_services(rag: BankingRAGService, chat: ChatService):
    """Set the service instances for the API routes."""
    global rag_service, chat_service
    rag_service = rag
    chat_service = chat

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
    start_time = time.time()

    try:
        # Get request data
        data = request.get_json()

        if not data or 'query' not in data:
            return jsonify({
                "status": "error",
                "message": "Missing 'query' field in request body"
            }), 400
        query = data['query'].strip() if 'query' in data else ''
        session_id = data.get('session_id')
        user_id = data.get('user_id', 'anonymous')
        # Allow empty query if session_id is provided (for chat history reload)
        if not query and not session_id:
            return jsonify({
                "status": "error",
                "message": "Query cannot be empty"
            }), 400

        # Auto-create session if none provided and chat service is available
        if chat_service and not session_id:
            try:
                session = chat_service.create_session(
                    user_id=user_id,
                    session_name=f"Banking Inquiry - {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                    metadata={"auto_created": True, "first_query": query[:100]}
                )
                session_id = session.id
                print(f"✅ Auto-created chat session: {session_id}")
            except Exception as e:
                print(f"⚠️  Failed to create chat session: {str(e)}")
                # Continue without chat history if creation fails
                session_id = None

        # Get existing session if session_id provided
        context_messages = []
        if chat_service and session_id:
            session = chat_service.get_session(session_id)
            if not session:
                return jsonify({
                    "status": "error",
                    "message": "Session not found"
                }), 404
            # Add user message to session only if content is not null or empty
            if query:
                try:
                    user_message = chat_service.add_message(session_id, 'user', query)
                    print(f"✅ Saved user message: {user_message.id}")
                except Exception as e:
                    print(f"⚠️  Failed to save user message: {str(e)}")
            # Get last N messages for short-term memory
            N = 10  # window size, can be configured
            all_messages = chat_service.get_session_messages(session_id, limit=N)

            context_messages = [msg.to_dict() for msg in all_messages]
            print(f"🔍 Short-term memory context contents: {[msg['content'] for msg in context_messages]}")

        # Process the query with short-term memory context
        result = rag_service.answer_question(query, context=context_messages)

        # Calculate response time
        response_time_ms = int((time.time() - start_time) * 1000)

        # Add assistant response to session if using chat history
        if chat_service and session_id and result.get('status') == 'success':
            try:
                assistant_message = chat_service.add_message(
                    session_id,
                    'assistant',
                    result['answer'],
                    sources=result.get('sources', []),
                    response_time_ms=response_time_ms
                )
                print(f"✅ Saved assistant message: {assistant_message.id}")
            except Exception as e:
                print(f"⚠️  Failed to save assistant message: {str(e)}")

        # Add response time, timestamp, and session info to result
        result['response_time_ms'] = response_time_ms
        result['timestamp'] = datetime.now().isoformat()
        # Include session information in response
        if session_id:
            result['session_id'] = session_id
            result['chat_enabled'] = True
            # Load all messages for this session
            if chat_service:
                messages = chat_service.get_session_messages(session_id)
                result['messages'] = [msg.to_dict() for msg in messages]
        else:
            result['chat_enabled'] = False
        return jsonify(result)

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

# Chat Session Management Endpoints

@api_blueprint.route('/chat/sessions', methods=['POST'])
def create_chat_session():
    """Create a new chat session."""
    if not chat_service:
        return jsonify({
            "status": "error",
            "message": "Chat service not available"
        }), 503
    
    try:
        data = request.get_json() or {}
        
        user_id = data.get('user_id')
        session_name = data.get('session_name')
        metadata = data.get('metadata', {})
        
        session = chat_service.create_session(
            user_id=user_id,
            session_name=session_name,
            metadata=metadata
        )
        
        return jsonify({
            "status": "success",
            "session": session.to_dict(),
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@api_blueprint.route('/chat/sessions/<session_id>', methods=['GET'])
def get_chat_session(session_id):
    """Get a specific chat session with its messages."""
    if not chat_service:
        return jsonify({
            "status": "error",
            "message": "Chat service not available"
        }), 503
    
    try:
        session = chat_service.get_session(session_id)
        
        if not session:
            return jsonify({
                "status": "error",
                "message": "Session not found"
            }), 404
        
        messages = chat_service.get_session_messages(session_id)
        
        return jsonify({
            "status": "success",
            "session": session.to_dict(),
            "messages": [msg.to_dict() for msg in messages],
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@api_blueprint.route('/chat/sessions/<session_id>', methods=['PUT'])
def update_chat_session(session_id):
    """Update a chat session."""
    if not chat_service:
        return jsonify({
            "status": "error",
            "message": "Chat service not available"
        }), 503
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "status": "error",
                "message": "Request body required"
            }), 400
        
        success = chat_service.update_session(
            session_id=session_id,
            session_name=data.get('session_name'),
            is_active=data.get('is_active'),
            metadata=data.get('metadata')
        )
        
        if success:
            session = chat_service.get_session(session_id)
            return jsonify({
                "status": "success",
                "session": session.to_dict(),
                "timestamp": datetime.now().isoformat()
            })
        else:
            return jsonify({
                "status": "error",
                "message": "Session not found"
            }), 404
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@api_blueprint.route('/chat/sessions/<session_id>/messages', methods=['GET'])
def get_session_messages(session_id):
    """Get messages for a specific session."""
    if not chat_service:
        return jsonify({
            "status": "error",
            "message": "Chat service not available"
        }), 503
    
    try:
        limit = request.args.get('limit', 100, type=int)
        messages = chat_service.get_session_messages(session_id, limit=limit)
        
        return jsonify({
            "status": "success",
            "session_id": session_id,
            "messages": [msg.to_dict() for msg in messages],
            "message_count": len(messages),
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@api_blueprint.route('/chat/messages/<message_id>/feedback', methods=['POST'])
def add_message_feedback(message_id):
    """Add feedback rating to a message."""
    if not chat_service:
        return jsonify({
            "status": "error",
            "message": "Chat service not available"
        }), 503
    
    try:
        data = request.get_json()
        
        if not data or 'rating' not in data:
            return jsonify({
                "status": "error",
                "message": "Missing 'rating' field in request body"
            }), 400
        
        rating = data['rating']
        
        if not isinstance(rating, int) or not 1 <= rating <= 5:
            return jsonify({
                "status": "error",
                "message": "Rating must be an integer between 1 and 5"
            }), 400
        
        success = chat_service.add_message_feedback(message_id, rating)
        
        if success:
            return jsonify({
                "status": "success",
                "message": "Feedback added successfully",
                "timestamp": datetime.now().isoformat()
            })
        else:
            return jsonify({
                "status": "error",
                "message": "Message not found"
            }), 404
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@api_blueprint.route('/chat/sessions/<session_id>/statistics', methods=['GET'])
def get_session_statistics(session_id):
    """Get statistics for a chat session."""
    if not chat_service:
        return jsonify({
            "status": "error",
            "message": "Chat service not available"
        }), 503
    
    try:
        stats = chat_service.get_session_statistics(session_id)
        
        if not stats:
            return jsonify({
                "status": "error",
                "message": "Session not found"
            }), 404
        
        return jsonify({
            "status": "success",
            "statistics": stats,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@api_blueprint.route('/chat/users/<user_id>/sessions', methods=['GET'])
def get_user_sessions(user_id):
    """Get chat sessions for a specific user."""
    if not chat_service:
        return jsonify({
            "status": "error",
            "message": "Chat service not available"
        }), 503
    
    try:
        limit = request.args.get('limit', 50, type=int)
        active_only = request.args.get('active_only', 'true').lower() == 'true'
        
        sessions = chat_service.get_user_sessions(
            user_id=user_id,
            limit=limit,
            active_only=active_only
        )
        
        return jsonify({
            "status": "success",
            "user_id": user_id,
            "sessions": [session.to_dict() for session in sessions],
            "session_count": len(sessions),
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

# Existing endpoints remain the same...

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
