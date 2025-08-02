"""
Banking Models

Data structures and models for the Banking RAG System.
"""

from dataclasses import dataclass
from typing import Optional
import numpy as np

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
