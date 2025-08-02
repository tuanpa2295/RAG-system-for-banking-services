#!/usr/bin/env python3
"""
Banking RAG Service

This module contains the core RAG functionality for banking Q&A,
including embedding generation, vector search, and response generation.

Author: GitHub Copilot
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
    """
    
    def __init__(self):
        """Initialize the Banking RAG service."""
        # Azure OpenAI configuration
        self.client = None
        self.embedding_model = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME", "text-embedding-3-small")
        self.chat_model = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "GPT-4o")
        
        # Update embedding dimension for text-embedding-3-small
        if "text-embedding-3-small" in self.embedding_model:
            self.embedding_dimension = 1536  # text-embedding-3-small dimension
        else:
            self.embedding_dimension = 1536  # default dimension
        
        # Storage
        self.documents: List[BankingDocument] = []
        self.index: Optional[faiss.IndexFlatIP] = None
        self.is_initialized = False
        
        # File paths
        self.index_file = "banking_vector_index.faiss"
        self.docs_file = "banking_vector_index_docs.pkl"
    
    def _setup_client(self):
        """Set up Azure OpenAI client."""
        try:
            api_key = os.getenv("AZURE_OPENAI_API_KEY")
            endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
            
            if not api_key or not endpoint:
                print("⚠️  Azure OpenAI credentials not found in environment")
                return False
            
            self.client = AzureOpenAI(
                api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01"),
                azure_endpoint=endpoint,
                api_key=api_key,
            )
            
            print("✅ Azure OpenAI client initialized successfully")
            return True
        except Exception as e:
            print(f"❌ Could not initialize Azure OpenAI client: {str(e)}")
            return False
    
    def initialize(self):
        """Initialize the RAG service."""
        print("Initializing Banking RAG Service...")
        
        # Set up client
        self._setup_client()
        
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
        """Generate embeddings for texts."""
        if not self.client:
            return self._generate_mock_embeddings(len(texts))
        
        try:
            embeddings = []
            batch_size = 10
            
            for i in range(0, len(texts), batch_size):
                batch = texts[i:i + batch_size]
                
                response = self.client.embeddings.create(
                    model=self.embedding_model,
                    input=batch
                )
                
                batch_embeddings = [np.array(embedding.embedding) for embedding in response.data]
                embeddings.extend(batch_embeddings)
            
            return embeddings
            
        except Exception as e:
            print(f"Error generating embeddings: {str(e)}")
            return self._generate_mock_embeddings(len(texts))
    
    def _generate_mock_embeddings(self, count: int) -> List[np.ndarray]:
        """Generate mock embeddings for demonstration."""
        print("Using mock embeddings for demonstration...")
        return [np.random.rand(self.embedding_dimension) for _ in range(count)]
    
    def _create_vector_index(self):
        """Create FAISS vector index."""
        print("Creating vector index...")
        
        # Generate embeddings for all documents
        document_texts = [f"{doc.title}\n{doc.content}" for doc in self.documents]
        embeddings = self._generate_embeddings(document_texts)
        
        # Store embeddings in documents
        for doc, embedding in zip(self.documents, embeddings):
            doc.embedding = embedding
        
        # Create FAISS index
        self.index = faiss.IndexFlatIP(self.embedding_dimension)
        
        # Normalize embeddings for cosine similarity
        embedding_matrix = np.vstack([doc.embedding for doc in self.documents]).astype('float32')
        norms = np.linalg.norm(embedding_matrix, axis=1, keepdims=True)
        embedding_matrix = embedding_matrix / (norms + 1e-8)
        
        # Add embeddings to index
        self.index.add(embedding_matrix)
        
        print(f"Vector index created with {len(self.documents)} documents")
    
    def _save_index(self):
        """Save the vector index and documents to disk."""
        try:
            if self.index:
                faiss.write_index(self.index, self.index_file)
            
            with open(self.docs_file, 'wb') as f:
                pickle.dump(self.documents, f)
            
            print(f"Index and documents saved to {self.index_file}")
        except Exception as e:
            print(f"Error saving index: {str(e)}")
    
    def _load_index(self) -> bool:
        """Load the vector index and documents from disk."""
        try:
            self.index = faiss.read_index(self.index_file)
            
            with open(self.docs_file, 'rb') as f:
                self.documents = pickle.load(f)
            
            print(f"Index and documents loaded from {self.index_file}")
            return True
        except Exception as e:
            print(f"Could not load index: {str(e)}")
            return False
    
    def retrieve_documents(self, query: str, top_k: int = 3) -> List[RetrievalResult]:
        """Retrieve relevant documents for a query."""
        if not self.index:
            return []
        
        try:
            # Generate query embedding
            query_embeddings = self._generate_embeddings([query])
            if not query_embeddings:
                return []
            
            query_vector = query_embeddings[0].reshape(1, -1).astype('float32')
            
            # Normalize query vector
            norm = np.linalg.norm(query_vector)
            if norm > 0:
                query_vector = query_vector / norm
            
            # Search for similar documents
            scores, indices = self.index.search(query_vector, top_k)
            
            # Create retrieval results
            results = []
            for rank, (score, idx) in enumerate(zip(scores[0], indices[0])):
                if idx < len(self.documents):
                    results.append(RetrievalResult(
                        document=self.documents[idx],
                        similarity_score=float(score),
                        relevance_rank=rank + 1
                    ))
            
            return results
            
        except Exception as e:
            print(f"Error during retrieval: {str(e)}")
            return self._mock_retrieval(query, top_k)
    
    def _mock_retrieval(self, query: str, top_k: int) -> List[RetrievalResult]:
        """Mock retrieval for demonstration."""
        print("Using mock retrieval for demonstration...")
        
        query_lower = query.lower()
        scored_docs = []
        
        for doc in self.documents:
            score = 0
            content_lower = f"{doc.title} {doc.content}".lower()
            
            keywords = query_lower.split()
            for keyword in keywords:
                if keyword in content_lower:
                    score += content_lower.count(keyword)
            
            if score > 0:
                scored_docs.append((doc, score))
        
        scored_docs.sort(key=lambda x: x[1], reverse=True)
        
        results = []
        for rank, (doc, score) in enumerate(scored_docs[:top_k]):
            results.append(RetrievalResult(
                document=doc,
                similarity_score=score / 10.0,
                relevance_rank=rank + 1
            ))
        
        return results
    
    def generate_response(self, query: str, retrieved_docs: List[RetrievalResult]) -> str:
        """Generate response using retrieved documents."""
        if not retrieved_docs:
            return "I apologize, but I couldn't find relevant information to answer your question. Please contact our customer service for assistance."
        
        # Prepare context
        context_parts = []
        for result in retrieved_docs:
            doc = result.document
            context_parts.append(f"Document: {doc.title}\nCategory: {doc.category}\nContent: {doc.content}")
        
        context = "\n\n".join(context_parts)
        
        # Create prompt
        system_prompt = """You are a knowledgeable banking and financial services assistant. 
Use the provided context to answer customer questions accurately and helpfully. 

Guidelines:
- Provide specific, actionable information based on the context
- Include relevant details like requirements, rates, or processes
- If information is not in the context, say so clearly  
- Maintain a professional, helpful tone
- Cite specific policies or requirements when applicable
- For sensitive financial matters, recommend speaking with a specialist"""

        user_prompt = f"""Context Information:
{context}

Customer Question: {query}

Please provide a comprehensive answer based on the context above."""

        if not self.client:
            return self._generate_mock_response(query, retrieved_docs)
        
        try:
            response = self.client.chat.completions.create(
                model=self.chat_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=800
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error generating response: {str(e)}")
            return self._generate_mock_response(query, retrieved_docs)
    
    def _generate_mock_response(self, query: str, retrieved_docs: List[RetrievalResult]) -> str:
        """Generate mock response for demonstration."""
        doc_titles = [result.document.title for result in retrieved_docs]
        return f"""Based on our banking policies and procedures, here's information about your question: "{query}"

**{retrieved_docs[0].document.title}** (Category: {retrieved_docs[0].document.category})

{retrieved_docs[0].document.content[:300]}...

For more detailed information and personalized assistance, I recommend speaking with one of our banking specialists who can provide specific guidance based on your individual situation.

Would you like me to help you with anything else regarding our banking services?"""
    
    def answer_question(self, query: str) -> Dict:
        """Complete Q&A pipeline."""
        if not self.is_initialized:
            self.initialize()
        
        # Retrieve relevant documents
        retrieved_docs = self.retrieve_documents(query, top_k=3)
        
        if not retrieved_docs:
            return {
                "status": "success",
                "query": query,
                "answer": "I couldn't find relevant information for your question. Please contact customer service.",
                "sources": [],
                "confidence": 0.0
            }
        
        # Generate response
        answer = self.generate_response(query, retrieved_docs)
        
        # Prepare sources
        sources = []
        for result in retrieved_docs:
            sources.append({
                "title": result.document.title,
                "category": result.document.category,
                "relevance_score": result.similarity_score,
                "source": result.document.source
            })
        
        return {
            "status": "success",
            "query": query,
            "answer": answer,
            "sources": sources,
            "confidence": retrieved_docs[0].similarity_score if retrieved_docs else 0.0
        }
    
    def get_health_status(self) -> Dict:
        """Get the health status of the RAG service."""
        return {
            "service": "Banking RAG Service",
            "status": "healthy" if self.is_initialized else "initializing",
            "documents_loaded": len(self.documents),
            "index_ready": self.index is not None,
            "embedding_model": self.embedding_model,
            "chat_model": self.chat_model
        }
    
    def add_document(self, document: BankingDocument) -> bool:
        """Add a new document to the knowledge base and update the index."""
        try:
            # Check if document ID already exists
            if any(doc.id == document.id for doc in self.documents):
                print(f"Document with ID {document.id} already exists")
                return False
            
            # Generate embedding for the new document
            text = f"{document.title}\n{document.content}"
            embeddings = self._generate_embeddings([text])
            
            if not embeddings:
                print("Failed to generate embedding for new document")
                return False
            
            document.embedding = embeddings[0]
            
            # Add to documents list
            self.documents.append(document)
            
            # Rebuild the index
            self.rebuild_index()
            
            print(f"Successfully added document: {document.title}")
            return True
            
        except Exception as e:
            print(f"Error adding document: {str(e)}")
            return False
    
    def remove_document(self, document_id: str) -> bool:
        """Remove a document from the knowledge base."""
        try:
            # Find and remove the document
            original_count = len(self.documents)
            self.documents = [doc for doc in self.documents if doc.id != document_id]
            
            if len(self.documents) == original_count:
                print(f"Document with ID {document_id} not found")
                return False
            
            # Rebuild the index
            self.rebuild_index()
            
            print(f"Successfully removed document: {document_id}")
            return True
            
        except Exception as e:
            print(f"Error removing document: {str(e)}")
            return False
    
    def rebuild_index(self):
        """Rebuild the vector index with current documents."""
        try:
            if not self.documents:
                print("No documents to index")
                return
            
            print(f"Rebuilding index with {len(self.documents)} documents...")
            
            # Create new index
            self.index = faiss.IndexFlatIP(self.embedding_dimension)
            
            # Collect embeddings (generate if missing)
            embeddings_to_add = []
            documents_to_reembed = []
            
            for doc in self.documents:
                if doc.embedding is not None:
                    embeddings_to_add.append(doc.embedding)
                else:
                    documents_to_reembed.append(doc)
            
            # Generate embeddings for documents that don't have them
            if documents_to_reembed:
                texts = [f"{doc.title}\n{doc.content}" for doc in documents_to_reembed]
                new_embeddings = self._generate_embeddings(texts)
                
                for doc, embedding in zip(documents_to_reembed, new_embeddings):
                    doc.embedding = embedding
                    embeddings_to_add.append(embedding)
            
            # Add all embeddings to index
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
