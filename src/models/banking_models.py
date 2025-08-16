"""
Banking Models

Data structures and models for the Banking RAG System.
"""

from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime
import numpy as np
import uuid
import os
from sqlalchemy import Column, String, Text, DateTime, Float, Integer, ForeignKey, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID

# SQLAlchemy Base
Base = declarative_base()

def get_uuid_column():
    """Get appropriate UUID column type based on database backend."""
    database_url = os.getenv('DATABASE_URL', '')
    if database_url.startswith('postgresql'):
        return Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    else:
        return Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

def get_uuid_foreign_key(table_column):
    """Get appropriate UUID foreign key column type based on database backend."""
    database_url = os.getenv('DATABASE_URL', '')
    if database_url.startswith('postgresql'):
        return Column(PostgresUUID(as_uuid=True), ForeignKey(table_column), nullable=False)
    else:
        return Column(String(36), ForeignKey(table_column), nullable=False)

# SQLAlchemy Base
Base = declarative_base()

class ChatSession(Base):
    """
    Represents a chat session between a user and the banking RAG system.
    
    Attributes:
        id: Unique session identifier (UUID)
        user_id: Optional user identifier for authenticated users
        session_name: Optional name for the session (e.g., "Loan Inquiry")
        created_at: When the session was created
        updated_at: When the session was last updated
        is_active: Whether the session is currently active
        metadata: Additional session information (JSON)
    """
    __tablename__ = 'chat_sessions'
    
    id = get_uuid_column()
    user_id = Column(String(50), nullable=True)  # For future user authentication
    session_name = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    session_metadata = Column(JSON, nullable=True)  # Store additional context/preferences
    
    # Relationship to messages
    messages = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan")
    
    def to_dict(self):
        """Convert session to dictionary format."""
        return {
            "id": str(self.id),  # Convert UUID to string
            "user_id": self.user_id,
            "session_name": self.session_name,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "is_active": self.is_active,
            "metadata": self.session_metadata,
            "message_count": len(self.messages) if self.messages else 0
        }

class ChatMessage(Base):
    """
    Represents a single message in a chat session.
    
    Attributes:
        id: Unique message identifier
        session_id: Reference to the chat session
        message_type: 'user' or 'assistant'
        content: The message content
        timestamp: When the message was created
        response_time_ms: Time taken to generate response (for assistant messages)
        sources: JSON array of source documents used (for assistant messages)
        feedback_rating: User rating of the response (1-5, nullable)
        metadata: Additional message information (JSON)
    """
    __tablename__ = 'chat_messages'
    
    id = get_uuid_column()
    session_id = get_uuid_foreign_key('chat_sessions.id')
    message_type = Column(String(20), nullable=False)  # 'user' or 'assistant'
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    response_time_ms = Column(Integer, nullable=True)  # For performance tracking
    sources = Column(JSON, nullable=True)  # RAG source documents
    feedback_rating = Column(Integer, nullable=True)  # 1-5 rating
    message_metadata = Column(JSON, nullable=True)
    
    # Relationship to session
    session = relationship("ChatSession", back_populates="messages")
    
    def to_dict(self):
        """Convert message to dictionary format."""
        return {
            "id": str(self.id),  # Convert UUID to string
            "session_id": str(self.session_id),  # Convert UUID to string
            "message_type": self.message_type,
            "content": self.content,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "response_time_ms": self.response_time_ms,
            "sources": self.sources,
            "feedback_rating": self.feedback_rating,
            "metadata": self.message_metadata
        }

class SessionSummary(Base):
    """
    Stores AI-generated summaries of chat sessions for quick reference.
    
    Attributes:
        id: Unique summary identifier
        session_id: Reference to the chat session
        summary: AI-generated summary of the conversation
        topics: List of main topics discussed
        created_at: When the summary was generated
        summary_type: Type of summary ('auto', 'manual')
    """
    __tablename__ = 'session_summaries'
    
    id = get_uuid_column()
    session_id = get_uuid_foreign_key('chat_sessions.id')
    summary = Column(Text, nullable=False)
    topics = Column(JSON, nullable=True)  # Array of topics
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    summary_type = Column(String(20), default='auto', nullable=False)
    
    # Relationship to session
    session = relationship("ChatSession")
    
    def to_dict(self):
        """Convert summary to dictionary format."""
        return {
            "id": str(self.id),  # Convert UUID to string
            "session_id": str(self.session_id),  # Convert UUID to string
            "summary": self.summary,
            "topics": self.topics,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "summary_type": self.summary_type
        }

# Original dataclasses for backward compatibility
@dataclass
class BankingDocument:
    """
    Represents a banking document in the knowledge base.
    
    Attributes:
        id: Unique identifier for the document
        title: Human-readable title of the document
        content: Full text content of the document
        category: Category classification (e.g., 'loans', 'accounts', 'support')
        source: Source filename or identifier
        embedding: Vector embedding of the document (optional)
        date_added: ISO format datetime when the document was added (optional)
    """
    id: str
    title: str
    content: str
    category: str
    source: str
    embedding: Optional[np.ndarray] = None
    date_added: Optional[str] = None
    
    def __post_init__(self):
        """Validate document fields after initialization."""
        if not self.id or not self.title or not self.content:
            raise ValueError("Document must have id, title, and content")
        
        if not self.category or not self.source:
            raise ValueError("Document must have category and source")

@dataclass
class RetrievalResult:
    """
    Represents a document retrieval result with relevance scoring.
    
    Attributes:
        document: The retrieved banking document
        relevance_score: Similarity score (0.0 to 1.0)
        rank: Ranking position in the retrieval results
    """
    document: BankingDocument
    relevance_score: float
    rank: int = 0
    
    def __post_init__(self):
        """Validate retrieval result fields."""
        if not isinstance(self.relevance_score, (int, float)):
            raise ValueError("Relevance score must be numeric")
        
        if not 0.0 <= self.relevance_score <= 1.0:
            raise ValueError("Relevance score must be between 0.0 and 1.0")

    def to_dict(self) -> dict:
        """Convert retrieval result to dictionary format."""
        return {
            "title": self.document.title,
            "category": self.document.category,
            "source": self.document.source,
            "relevance_score": self.relevance_score,
            "rank": self.rank
        }
