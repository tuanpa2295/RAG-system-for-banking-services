"""
Chat Service

Database service for managing chat sessions and messages.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy import create_engine, and_, or_, desc
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
import json
import logging
import os
import uuid

from .banking_models import Base, ChatSession, ChatMessage, SessionSummary

logger = logging.getLogger(__name__)

class ChatService:
    """Service class for managing chat sessions and messages."""
    
    def __init__(self, database_url: str = None):
        """
        Initialize the chat service.
        
        Args:
            database_url: SQLAlchemy database URL. If None, uses env var.
        """
        # Always use DATABASE_URL from environment
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            raise RuntimeError("DATABASE_URL environment variable must be set for PostgreSQL connection.")
        self.engine = create_engine(database_url, echo=False)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        # Create tables if they don't exist
        self.create_tables()
    
    def create_tables(self):
        """Create all database tables."""
        try:
            Base.metadata.create_all(bind=self.engine)
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Failed to create database tables: {str(e)}")
            raise
    
    def get_db_session(self) -> Session:
        """Get a database session."""
        return self.SessionLocal()
    
    def _convert_to_uuid(self, uuid_string: str):
        """Convert string UUID to UUID object if using PostgreSQL."""
        try:
            if isinstance(uuid_string, str):
                return uuid.UUID(uuid_string)
            return uuid_string
        except (ValueError, TypeError):
            return uuid_string
    
    # Session Management Methods
    
    def create_session(self, user_id: str = None, session_name: str = None, 
                      metadata: Dict[str, Any] = None) -> ChatSession:
        """
        Create a new chat session.
        
        Args:
            user_id: Optional user identifier
            session_name: Optional name for the session
            metadata: Additional session information
            
        Returns:
            Created ChatSession object
        """
        db = self.get_db_session()
        try:
            session = ChatSession(
                user_id=user_id,
                session_name=session_name,
                session_metadata=metadata
            )
            db.add(session)
            db.commit()
            db.refresh(session)
            logger.info(f"Created new chat session: {session.id}")
            return session
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Failed to create chat session: {str(e)}")
            raise
        finally:
            db.close()
    
    def get_session(self, session_id: str) -> Optional[ChatSession]:
        """
        Get a chat session by ID.
        
        Args:
            session_id: Session identifier
            
        Returns:
            ChatSession object or None if not found
        """
        db = self.get_db_session()
        try:
            # Convert string UUID to UUID object if needed
            uuid_id = self._convert_to_uuid(session_id)
            session = db.query(ChatSession).filter(ChatSession.id == uuid_id).first()
            return session
        except SQLAlchemyError as e:
            logger.error(f"Failed to get chat session {session_id}: {str(e)}")
            return None
        finally:
            db.close()
    
    def get_user_sessions(self, user_id: str, limit: int = 50, 
                         active_only: bool = True) -> List[ChatSession]:
        """
        Get chat sessions for a specific user.
        
        Args:
            user_id: User identifier
            limit: Maximum number of sessions to return
            active_only: Whether to return only active sessions
            
        Returns:
            List of ChatSession objects
        """
        db = self.get_db_session()
        try:
            query = db.query(ChatSession).filter(ChatSession.user_id == user_id)
            
            if active_only:
                query = query.filter(ChatSession.is_active == True)
            
            sessions = query.order_by(desc(ChatSession.updated_at)).limit(limit).all()
            return sessions
        except SQLAlchemyError as e:
            logger.error(f"Failed to get user sessions for {user_id}: {str(e)}")
            return []
        finally:
            db.close()
    
    def update_session(self, session_id: str, session_name: str = None, 
                      is_active: bool = None, metadata: Dict[str, Any] = None) -> bool:
        """
        Update a chat session.
        
        Args:
            session_id: Session identifier
            session_name: New session name
            is_active: New active status
            metadata: New metadata
            
        Returns:
            True if updated successfully, False otherwise
        """
        db = self.get_db_session()
        try:
            uuid_id = self._convert_to_uuid(session_id)
            session = db.query(ChatSession).filter(ChatSession.id == uuid_id).first()
            if not session:
                return False
            
            if session_name is not None:
                session.session_name = session_name
            if is_active is not None:
                session.is_active = is_active
            if metadata is not None:
                session.session_metadata = metadata
            
            session.updated_at = datetime.utcnow()
            db.commit()
            logger.info(f"Updated chat session: {session_id}")
            return True
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Failed to update chat session {session_id}: {str(e)}")
            return False
        finally:
            db.close()
    
    # Message Management Methods
    
    def add_message(self, session_id: str, message_type: str, content: str,
                   sources: List[Dict[str, Any]] = None, response_time_ms: int = None,
                   metadata: Dict[str, Any] = None) -> Optional[ChatMessage]:
        """
        Add a message to a chat session.
        
        Args:
            session_id: Session identifier
            message_type: 'user' or 'assistant'
            content: Message content
            sources: RAG source documents (for assistant messages)
            response_time_ms: Response generation time
            metadata: Additional message information
            
        Returns:
            Created ChatMessage object or None if failed
        """
        db = self.get_db_session()
        try:
            # Verify session exists
            uuid_id = self._convert_to_uuid(session_id)
            session = db.query(ChatSession).filter(ChatSession.id == uuid_id).first()
            if not session:
                logger.error(f"Session {session_id} not found")
                return None
            
            message = ChatMessage(
                session_id=uuid_id,
                message_type=message_type,
                content=content,
                sources=sources,
                response_time_ms=response_time_ms,
                message_metadata=metadata
            )
            
            db.add(message)
            
            # Update session timestamp
            session.updated_at = datetime.utcnow()
            
            db.commit()
            db.refresh(message)
            logger.info(f"Added message to session {session_id}")
            return message
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Failed to add message to session {session_id}: {str(e)}")
            return None
        finally:
            db.close()
    
    def get_session_messages(self, session_id: str, limit: int = 100) -> List[ChatMessage]:
        """
        Get messages for a chat session.
        
        Args:
            session_id: Session identifier
            limit: Maximum number of messages to return
            
        Returns:
            List of ChatMessage objects ordered by timestamp
        """
        db = self.get_db_session()
        try:
            uuid_id = self._convert_to_uuid(session_id)
            messages = (db.query(ChatMessage)
                       .filter(ChatMessage.session_id == uuid_id)
                       .order_by(ChatMessage.timestamp)
                       .limit(limit)
                       .all())
            return messages
        except SQLAlchemyError as e:
            logger.error(f"Failed to get messages for session {session_id}: {str(e)}")
            return []
        finally:
            db.close()
    
    def add_message_feedback(self, message_id: str, rating: int) -> bool:
        """
        Add feedback rating to a message.
        
        Args:
            message_id: Message identifier
            rating: Rating from 1-5
            
        Returns:
            True if updated successfully, False otherwise
        """
        db = self.get_db_session()
        try:
            if not 1 <= rating <= 5:
                logger.error(f"Invalid rating: {rating}. Must be 1-5.")
                return False
            
            message = db.query(ChatMessage).filter(ChatMessage.id == message_id).first()
            if not message:
                return False
            
            message.feedback_rating = rating
            db.commit()
            logger.info(f"Added feedback rating {rating} to message {message_id}")
            return True
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Failed to add feedback to message {message_id}: {str(e)}")
            return False
        finally:
            db.close()
    
    # Analytics and Summary Methods
    
    def get_session_statistics(self, session_id: str) -> Dict[str, Any]:
        """
        Get statistics for a chat session.
        
        Args:
            session_id: Session identifier
            
        Returns:
            Dictionary with session statistics
        """
        db = self.get_db_session()
        try:
            uuid_id = self._convert_to_uuid(session_id)
            session = db.query(ChatSession).filter(ChatSession.id == uuid_id).first()
            if not session:
                return {}
            
            messages = db.query(ChatMessage).filter(ChatMessage.session_id == uuid_id).all()
            
            user_messages = [m for m in messages if m.message_type == 'user']
            assistant_messages = [m for m in messages if m.message_type == 'assistant']
            
            # Calculate average response time
            response_times = [m.response_time_ms for m in assistant_messages if m.response_time_ms]
            avg_response_time = sum(response_times) / len(response_times) if response_times else 0
            
            # Calculate average rating
            ratings = [m.feedback_rating for m in assistant_messages if m.feedback_rating]
            avg_rating = sum(ratings) / len(ratings) if ratings else None
            
            return {
                "session_id": session_id,
                "created_at": session.created_at.isoformat(),
                "duration_minutes": (session.updated_at - session.created_at).total_seconds() / 60,
                "total_messages": len(messages),
                "user_messages": len(user_messages),
                "assistant_messages": len(assistant_messages),
                "average_response_time_ms": avg_response_time,
                "average_rating": avg_rating,
                "has_feedback": len(ratings) > 0
            }
        except SQLAlchemyError as e:
            logger.error(f"Failed to get statistics for session {session_id}: {str(e)}")
            return {}
        finally:
            db.close()
    
    def cleanup_old_sessions(self, days_old: int = 30) -> int:
        """
        Clean up old inactive sessions.
        
        Args:
            days_old: Number of days after which to consider sessions old
            
        Returns:
            Number of sessions deleted
        """
        db = self.get_db_session()
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days_old)
            
            old_sessions = (db.query(ChatSession)
                          .filter(and_(
                              ChatSession.is_active == False,
                              ChatSession.updated_at < cutoff_date
                          ))
                          .all())
            
            count = len(old_sessions)
            
            for session in old_sessions:
                db.delete(session)
            
            db.commit()
            logger.info(f"Cleaned up {count} old sessions")
            return count
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Failed to cleanup old sessions: {str(e)}")
            return 0
        finally:
            db.close()
