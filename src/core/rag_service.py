#!/usr/bin/env python3
"""
Banking RAG Service

Core RAG functionality for banking Q&A, including embedding generation,
vector search, and response generation.

Author: Banking RAG Team
Date: August 2, 2025
"""

import os
import json
import numpy as np
import faiss
import pickle
from typing import List, Dict, Optional
from openai import AzureOpenAI
from dotenv import load_dotenv

from models import BankingDocument, RetrievalResult, get_banking_knowledge_base

# Load environment variables
load_dotenv()

class BankingRAGService:
    """
    Core RAG service for banking and financial services Q&A.
    
    This service handles:
    - Document embedding and indexing
    - Semantic search and retrieval
    - AI-powered response generation
    - Knowledge base management
    """
    
    def __init__(self):
        """Initialize the Banking RAG Service with dual Azure OpenAI clients."""
        # Load environment variables
        load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '..', 'config', '.env'))
        
        # Azure OpenAI configuration for embeddings
        self.embedding_api_key = os.getenv('AZURE_OPENAI_EMBEDDING_API_KEY')
        self.embedding_endpoint = os.getenv('AZURE_OPENAI_EMBEDDING_ENDPOINT')
        self.embedding_model = os.getenv('AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME', 'text-embedding-3-small')
        
        # Azure OpenAI configuration for chat completions
        self.chat_api_key = os.getenv('AZURE_OPENAI_CHAT_API_KEY')
        self.chat_endpoint = os.getenv('AZURE_OPENAI_CHAT_ENDPOINT')
        self.chat_model = os.getenv('AZURE_OPENAI_CHAT_DEPLOYMENT_NAME', 'GPT-4o-mini')
        
        self.api_version = os.getenv('AZURE_OPENAI_API_VERSION', '2024-02-01')
        
        # Initialize dual Azure OpenAI clients
        self.embedding_client = None
        self.chat_client = None
        
        if self.embedding_api_key and self.embedding_endpoint:
            self.embedding_client = AzureOpenAI(
                api_key=self.embedding_api_key,
                api_version=self.api_version,
                azure_endpoint=self.embedding_endpoint
            )
        
        if self.chat_api_key and self.chat_endpoint:
            self.chat_client = AzureOpenAI(
                api_key=self.chat_api_key,
                api_version=self.api_version,
                azure_endpoint=self.chat_endpoint
            )
        
        # Initialize knowledge base and vector store
        self.knowledge_base = get_banking_knowledge_base()
        self.vector_index = None
        self.document_map = {}
        self.documents = []
        self.index = None
        self.is_initialized = False
        
        # Initialize properties for file paths
        self.embedding_dimension = 1536  # text-embedding-3-small dimension
        self.index_file = "data/banking_faiss_index.idx"
        self.docs_file = "data/banking_documents.pkl"
        
        # Initialize the service
        self.initialize()
    
    def initialize(self):
        """Initialize the RAG service."""
        print("Initializing Banking RAG Service...")
        
        # Validate clients
        if not self.embedding_client:
            print("⚠️  Embedding client not initialized - check AZURE_OPENAI_EMBEDDING_API_KEY")
        else:
            print("✅ Embedding client initialized successfully")
            
        if not self.chat_client:
            print("⚠️  Chat client not initialized - check AZURE_OPENAI_CHAT_API_KEY")
        else:
            print("✅ Chat client initialized successfully")
        
        # Try to load existing index
        if self._load_index():
            print(f"Service initialized with {len(self.documents)} documents")
        else:
            print("Creating new knowledge base and vector index...")
            self._create_knowledge_base()
            self._create_vector_index()
            self._save_index()
            print(f"Service initialized with {len(self.documents)} documents")
        
        self.is_initialized = True
    
    def _create_knowledge_base(self):
        """Create the banking knowledge base."""
        self.documents = get_banking_knowledge_base()
    
    def _generate_embeddings(self, texts: List[str]) -> List[np.ndarray]:
        """Generate embeddings for texts using Azure OpenAI."""
        if not self.embedding_client:
            raise ValueError("Embedding client not initialized. Cannot generate embeddings.")
        
        try:
            embeddings = []
            batch_size = 10
            
            for i in range(0, len(texts), batch_size):
                batch = texts[i:i + batch_size]
                
                response = self.embedding_client.embeddings.create(
                    model=self.embedding_model,
                    input=batch
                )
                
                batch_embeddings = [np.array(embedding.embedding) for embedding in response.data]
                embeddings.extend(batch_embeddings)
            
            return embeddings
            
        except Exception as e:
            print(f"Error generating embeddings: {str(e)}")
            raise Exception(f"Failed to generate embeddings: {str(e)}")
    
    def _create_vector_index(self):
        """Create FAISS vector index from documents."""
        if not self.documents:
            raise ValueError("No documents to index")
        
        print("Creating vector index...")
        
        # Generate embeddings for all document contents
        texts = [doc.content for doc in self.documents]
        embeddings = self._generate_embeddings(texts)
        
        # Store embeddings in documents
        for doc, embedding in zip(self.documents, embeddings):
            doc.embedding = embedding
        
        # Create FAISS index
        self.index = faiss.IndexFlatIP(self.embedding_dimension)
        
        # Prepare embeddings matrix
        embedding_matrix = np.vstack(embeddings).astype('float32')
        
        # Normalize embeddings for cosine similarity
        norms = np.linalg.norm(embedding_matrix, axis=1, keepdims=True)
        embedding_matrix = embedding_matrix / (norms + 1e-8)
        
        # Add to index
        self.index.add(embedding_matrix)
        
        print(f"Vector index created with {len(self.documents)} documents")
    
    def _save_index(self):
        """Save vector index and documents to disk."""
        try:
            # Ensure data directory exists
            os.makedirs("data", exist_ok=True)
            
            # Save FAISS index
            faiss.write_index(self.index, self.index_file)
            
            # Save documents
            with open(self.docs_file, 'wb') as f:
                pickle.dump(self.documents, f)
            
            print(f"Index and documents saved to {self.index_file}")
        except Exception as e:
            print(f"Error saving index: {str(e)}")
    
    def _load_index(self) -> bool:
        """Load vector index and documents from disk."""
        try:
            if not os.path.exists(self.index_file) or not os.path.exists(self.docs_file):
                print(f"Could not load index: Files not found")
                return False
            
            # Load FAISS index
            self.index = faiss.read_index(self.index_file)
            
            # Load documents
            with open(self.docs_file, 'rb') as f:
                self.documents = pickle.load(f)
            
            print(f"Index and documents loaded from {self.index_file}")
            return True
        except Exception as e:
            print(f"Could not load index: {str(e)}")
            return False
    
    def retrieve_documents(self, query: str, top_k: int = 3) -> List[RetrievalResult]:
        """
        Retrieve most relevant documents for a query.
        
        Args:
            query: User query string
            top_k: Number of documents to retrieve
            
        Returns:
            List of RetrievalResult objects with documents and similarity scores
        """
        if not self.is_initialized or not self.index:
            raise ValueError("Service not initialized")
        
        if not self.embedding_client:
            raise ValueError("Embedding client not initialized. Cannot perform document retrieval.")
        
        try:
            # Generate query embedding
            query_embeddings = self._generate_embeddings([query])
            query_embedding = query_embeddings[0]
            
            # Normalize query embedding
            query_embedding = query_embedding / (np.linalg.norm(query_embedding) + 1e-8)
            
            # Search similar documents
            similarities, indices = self.index.search(
                query_embedding.reshape(1, -1).astype('float32'), 
                top_k
            )
            
            # Create retrieval results
            results = []
            for i, (similarity, doc_idx) in enumerate(zip(similarities[0], indices[0])):
                if doc_idx < len(self.documents):  # Valid index
                    result = RetrievalResult(
                        document=self.documents[doc_idx],
                        relevance_score=float(similarity),
                        rank=i + 1
                    )
                    results.append(result)
            
            return results
            
        except Exception as e:
            print(f"Error in document retrieval: {str(e)}")
            raise Exception(f"Failed to retrieve documents: {str(e)}")

    def generate_response(self, query: str, retrieved_docs: List[RetrievalResult]) -> str:
        """
        Generate AI response based on query and retrieved documents.
        
        Args:
            query: User query
            retrieved_docs: List of relevant documents
            
        Returns:
            Generated response string
        """
        if not self.chat_client:
            raise ValueError("Chat client not initialized. Cannot generate response.")
        
        try:
            # Prepare context from retrieved documents
            context_parts = []
            for result in retrieved_docs:
                doc = result.document
                context_parts.append(f"Document: {doc.title} ({doc.category})\nContent: {doc.content}\n")
            
            context = "\n".join(context_parts)
            
            # Create prompt
            prompt = f"""You are a helpful banking assistant with access to comprehensive banking and financial services information. Use the provided context to answer the user's question accurately and helpfully.

Context:
{context}

User Question: {query}

Instructions:
- Provide a clear, accurate answer based on the context provided
- If the context doesn't contain enough information, say so honestly
- Include specific details like rates, requirements, or processes when available
- Use a professional but friendly tone
- Keep the response concise but comprehensive

Answer:"""

            # Generate response using Azure OpenAI
            response = self.chat_client.chat.completions.create(
                model=self.chat_model,
                messages=[
                    {"role": "system", "content": "You are a helpful banking assistant providing accurate information about banking and financial services."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.3
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error generating response: {str(e)}")
            raise Exception(f"Failed to generate response: {str(e)}")
    
    def answer_question(self, query: str) -> Dict:
        """
        Main method to answer a banking question.
        
        Args:
            query: User question
            
        Returns:
            Dictionary with answer, sources, and metadata
        """
        try:
            if not self.is_initialized:
                self.initialize()
            
            # Retrieve relevant documents
            retrieved_docs = self.retrieve_documents(query, top_k=3)
            
            # Generate response
            answer = self.generate_response(query, retrieved_docs)
            
            # Calculate average confidence
            if retrieved_docs:
                avg_confidence = sum(r.relevance_score for r in retrieved_docs) / len(retrieved_docs)
            else:
                avg_confidence = 0.0
            
            # Prepare sources
            sources = [
                {
                    "title": result.document.title,
                    "category": result.document.category,
                    "source": result.document.source,
                    "relevance_score": result.relevance_score
                }
                for result in retrieved_docs
            ]
            
            return {
                "status": "success",
                "answer": answer,
                "confidence": avg_confidence,
                "sources": sources,
                "query": query
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "query": query
            }
    
    def get_health_status(self) -> Dict:
        """Get service health status."""
        return {
            "service": "Banking RAG Service",
            "status": "healthy" if self.is_initialized else "initializing",
            "documents_loaded": len(self.documents),
            "index_ready": self.index is not None,
            "embedding_model": self.embedding_model,
            "chat_model": self.chat_model
        }
    
    def add_document(self, document: BankingDocument) -> bool:
        """Add a new document to the knowledge base."""
        try:
            # Check if document already exists
            existing_ids = [doc.id for doc in self.documents]
            if document.id in existing_ids:
                print(f"Document with ID {document.id} already exists")
                return False
            
            # Generate embedding for the new document
            embeddings = self._generate_embeddings([document.content])
            document.embedding = embeddings[0]
            
            # Add to documents list
            self.documents.append(document)
            
            # Update the index
            if self.index is not None:
                # Normalize embedding
                embedding = document.embedding / (np.linalg.norm(document.embedding) + 1e-8)
                
                # Add to index
                self.index.add(embedding.reshape(1, -1).astype('float32'))
            
            # Save updated index
            self._save_index()
            
            print(f"Document '{document.title}' added successfully")
            return True
            
        except Exception as e:
            print(f"Error adding document: {str(e)}")
            return False
    
    def remove_document(self, document_id: str) -> bool:
        """Remove a document from the knowledge base."""
        try:
            # Find document
            doc_index = None
            for i, doc in enumerate(self.documents):
                if doc.id == document_id:
                    doc_index = i
                    break
            
            if doc_index is None:
                print(f"Document with ID {document_id} not found")
                return False
            
            # Remove from documents list
            removed_doc = self.documents.pop(doc_index)
            
            # Rebuild index (FAISS doesn't support efficient single item removal)
            self._create_vector_index()
            self._save_index()
            
            print(f"Document '{removed_doc.title}' removed successfully")
            return True
            
        except Exception as e:
            print(f"Error removing document: {str(e)}")
            return False
    
    def rebuild_index(self):
        """Rebuild the vector index from current documents."""
        try:
            print("Rebuilding vector index...")
            
            # Reload knowledge base to get any updates
            self._create_knowledge_base()
            
            # Handle existing documents that might not be in the knowledge base
            existing_docs = [doc for doc in self.documents if doc.id not in [d.id for d in get_banking_knowledge_base()]]
            
            # Combine knowledge base with existing custom documents
            all_docs = get_banking_knowledge_base() + existing_docs
            self.documents = all_docs
            
            # Generate embeddings for documents that don't have them
            documents_to_reembed = [doc for doc in self.documents if doc.embedding is None]
            
            if documents_to_reembed:
                texts_to_embed = [doc.content for doc in documents_to_reembed]
                new_embeddings = self._generate_embeddings(texts_to_embed)
                
                for doc, embedding in zip(documents_to_reembed, new_embeddings):
                    doc.embedding = embedding
            
            # Create new index
            self.index = faiss.IndexFlatIP(self.embedding_dimension)
            
            # Collect all embeddings
            embeddings_to_add = []
            for doc in self.documents:
                if doc.embedding is not None:
                    embeddings_to_add.append(doc.embedding)
                else:
                    # Generate embedding if missing
                    embeddings = self._generate_embeddings([doc.content])
                    doc.embedding = embeddings[0]
                    embeddings_to_add.append(doc.embedding)
            
            if embeddings_to_add:
                embedding_matrix = np.vstack(embeddings_to_add).astype('float32')
                
                # Normalize for cosine similarity
                norms = np.linalg.norm(embedding_matrix, axis=1, keepdims=True)
                embedding_matrix = embedding_matrix / (norms + 1e-8)
                
                self.index.add(embedding_matrix)
            
            # Save the updated index
            self._save_index()
            
            print(f"Index rebuilt successfully with {len(self.documents)} documents")
            
        except Exception as e:
            print(f"Error rebuilding index: {str(e)}")
            raise
    
    def list_documents(self) -> List[dict]:
        """List all documents in the knowledge base."""
        return [
            {
                "id": doc.id,
                "title": doc.title,
                "category": doc.category,
                "source": doc.source,
                "content_length": len(doc.content)
            }
            for doc in self.documents
        ]
