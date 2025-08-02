"""
Models package for the Banking RAG System.

This package contains data models and knowledge base definitions.
"""

from .banking_models import BankingDocument, RetrievalResult
from .knowledge_base import get_banking_knowledge_base

__all__ = [
    'BankingDocument',
    'RetrievalResult', 
    'get_banking_knowledge_base'
]
