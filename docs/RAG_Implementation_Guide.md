# Banking RAG System - Step-by-Step Guide

## Overview
This guide demonstrates how to implement a complete RAG (Retrieval-Augmented Generation) system for banking and financial services Q&A using Azure OpenAI embeddings and vector search.

## Prerequisites
```bash
pip install openai numpy faiss-cpu scikit-learn pandas
# or for GPU support: pip install faiss-gpu
```

## Architecture Overview

```
User Query → Embedding → Vector Search → Document Retrieval → Context + Query → LLM → Final Answer
     ↓             ↓            ↓              ↓                    ↓           ↓
  "How to get    Query        FAISS         Top-K Most        RAG Prompt    Generated
   a loan?"    Embedding      Index         Relevant Docs      Template      Response
```

## Step-by-Step Implementation

### Step 1: Create Banking Knowledge Base

```python
# Create structured documents for banking domain
banking_docs = [
    {
        "id": "doc_001",
        "title": "Personal Loan Requirements", 
        "content": "Loan requirements: age 21-65, income $3000+, credit score 650+...",
        "category": "loans",
        "source": "lending_policies.pdf"
    },
    # ... more documents
]
```

**Key Categories:**
- `loans` - Personal loans, mortgages, auto loans
- `accounts` - Savings, checking, money market accounts  
- `credit` - Credit cards, credit lines
- `investments` - IRAs, brokerage accounts, mutual funds
- `security` - Mobile banking, fraud protection
- `business` - Business banking services
- `regulations` - Compliance, federal banking laws
- `rates` - Interest rates, fee structures
- `support` - Customer service channels

### Step 2: Generate Embeddings

```python
def generate_embeddings(self, texts: List[str]) -> List[np.ndarray]:
    """Generate embeddings using Azure OpenAI text-embedding-ada-002"""
    
    embeddings = []
    batch_size = 10  # Process in batches
    
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        
        response = self.client.embeddings.create(
            model="text-embedding-ada-002",  # 1536 dimensions
            input=batch
        )
        
        batch_embeddings = [np.array(emb.embedding) for emb in response.data]
        embeddings.extend(batch_embeddings)
    
    return embeddings
```

**Embedding Strategy:**
- Combine title + content for richer embeddings
- Use batch processing to optimize API calls
- Normalize vectors for cosine similarity
- Store embeddings with document metadata

### Step 3: Create Vector Index (FAISS)

```python
def create_vector_index(self):
    """Create FAISS index for fast similarity search"""
    
    # Generate embeddings for all documents
    document_texts = [f"{doc.title}\n{doc.content}" for doc in self.documents]
    embeddings = self.generate_embeddings(document_texts)
    
    # Create FAISS index (Inner Product for cosine similarity)
    self.index = faiss.IndexFlatIP(1536)  # Ada-002 dimension
    
    # Normalize embeddings for cosine similarity
    embedding_matrix = np.vstack(embeddings)
    faiss.normalize_L2(embedding_matrix)
    
    # Add to index
    self.index.add(embedding_matrix.astype('float32'))
```

**Index Types:**
- `IndexFlatIP` - Exact search with inner product
- `IndexIVFFlat` - Faster approximate search for large datasets
- `IndexFlatL2` - L2 distance (Euclidean)
- `IndexHNSWFlat` - Hierarchical navigable small world graphs

### Step 4: Retrieve Relevant Documents

```python
def retrieve_documents(self, query: str, top_k: int = 3) -> List[RetrievalResult]:
    """Retrieve most relevant documents using vector similarity"""
    
    # Generate query embedding
    query_embeddings = self.generate_embeddings([query])
    query_vector = query_embeddings[0].reshape(1, -1).astype('float32')
    faiss.normalize_L2(query_vector)
    
    # Search for similar documents
    scores, indices = self.index.search(query_vector, top_k)
    
    # Return ranked results
    results = []
    for rank, (score, idx) in enumerate(zip(scores[0], indices[0])):
        results.append(RetrievalResult(
            document=self.documents[idx],
            similarity_score=float(score),
            relevance_rank=rank + 1
        ))
    
    return results
```

**Retrieval Strategies:**
- **Semantic Search**: Vector similarity for meaning-based matching
- **Hybrid Search**: Combine vector + keyword search
- **Re-ranking**: Use cross-encoder models for better ranking
- **Filtering**: Category-based filtering for domain-specific queries

### Step 5: Generate RAG Response

```python
def generate_rag_response(self, query: str, retrieved_docs: List[RetrievalResult]) -> str:
    """Generate response using retrieved context"""
    
    # Prepare context from retrieved documents
    context_parts = []
    for result in retrieved_docs:
        doc = result.document
        context_parts.append(f"Document: {doc.title}\nContent: {doc.content}")
    
    context = "\n\n".join(context_parts)
    
    # RAG prompt template
    system_prompt = """You are a banking assistant. Use the provided context 
    to answer questions accurately. Include specific requirements, rates, and 
    processes. If unsure, recommend speaking with a specialist."""
    
    user_prompt = f"""Context: {context}\n\nQuestion: {query}\n\nAnswer:"""
    
    # Generate response
    response = self.client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.3,  # Lower for factual responses
        max_tokens=800
    )
    
    return response.choices[0].message.content.strip()
```

**RAG Prompt Engineering:**
- **System Message**: Define role and guidelines
- **Context Injection**: Provide relevant documents as context
- **Query Formatting**: Structure the user question clearly
- **Temperature Control**: Lower values for factual accuracy
- **Token Management**: Balance context length vs. response quality

### Step 6: Complete Q&A Pipeline

```python
def answer_question(self, query: str) -> Dict:
    """End-to-end Q&A pipeline"""
    
    # 1. Retrieve relevant documents
    retrieved_docs = self.retrieve_documents(query, top_k=3)
    
    # 2. Generate response with context
    answer = self.generate_rag_response(query, retrieved_docs)
    
    # 3. Return structured response
    return {
        "query": query,
        "answer": answer,
        "sources": [{"title": r.document.title, "score": r.similarity_score} 
                   for r in retrieved_docs],
        "confidence": retrieved_docs[0].similarity_score if retrieved_docs else 0.0
    }
```

## Sample Banking Questions & Expected Flow

### Example 1: Personal Loan Inquiry
**Query**: "What are the requirements for getting a personal loan?"

**Retrieval Process**:
1. Query → Embedding vector
2. Vector search finds "Personal Loan Requirements" document (score: 0.89)
3. Also retrieves "Credit Application Process" (score: 0.76)
4. Context includes loan requirements, credit scores, income verification

**Generated Response**:
```
Based on our lending policies, personal loan requirements include:

- Minimum age: 21 years (maximum 65 at loan maturity)
- Monthly income: $3,000 minimum
- Credit score: 650 minimum (higher scores get better rates)
- Employment history: 2+ years
- Debt-to-income ratio: Below 40%
- Required documents: Pay stubs, tax returns, bank statements

Loan amounts range from $1,000 to $100,000 with terms from 12 to 84 months. 
Interest rates vary from 5.99% to 24.99% APR based on your creditworthiness.

I recommend speaking with our loan specialists for a personalized assessment.
```

### Example 2: Investment Account Query
**Query**: "What investment options do you offer?"

**Retrieval Process**:
1. Finds "Investment Account Options" document (score: 0.92)
2. Related documents on rates and account requirements
3. Context includes IRA options, minimum deposits, advisory services

**Generated Response**:
```
We offer several investment account options:

**Retirement Accounts:**
- Individual Retirement Account (IRA) - $500 minimum
- Roth IRA - $500 minimum  
- 401(k) rollover services

**Investment Accounts:**
- Brokerage accounts - $1,000 minimum
- Mutual funds and ETFs
- Certificate of Deposits (CDs) - $100 minimum

**Additional Services:**
- Investment advisory with certified financial planners
- Risk assessment and portfolio recommendations
- Online trading platform with research tools
- Educational resources and market analysis

Our advisors can help create a personalized investment strategy based on 
your age, income, and retirement goals.
```

## Advanced RAG Techniques

### 1. Hybrid Search
Combine vector similarity with keyword matching:
```python
def hybrid_search(self, query: str, alpha: float = 0.7):
    """Combine semantic and lexical search"""
    
    # Vector search scores
    vector_results = self.vector_search(query)
    
    # Keyword search scores (BM25)
    keyword_results = self.keyword_search(query)
    
    # Combine scores
    combined_scores = {}
    for doc_id, score in vector_results.items():
        combined_scores[doc_id] = alpha * score + (1 - alpha) * keyword_results.get(doc_id, 0)
    
    return sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)
```

### 2. Query Expansion
Enhance queries with banking-specific terms:
```python
def expand_query(self, query: str) -> str:
    """Expand query with domain-specific terms"""
    
    banking_synonyms = {
        "loan": ["credit", "financing", "borrowing"],
        "account": ["deposit", "savings", "checking"],
        "rate": ["APR", "interest", "percentage"],
        "apply": ["application", "qualification", "requirements"]
    }
    
    expanded_terms = []
    for word in query.lower().split():
        if word in banking_synonyms:
            expanded_terms.extend(banking_synonyms[word])
    
    return query + " " + " ".join(expanded_terms)
```

### 3. Context Window Management
Handle long documents with chunking:
```python
def chunk_document(self, document: str, chunk_size: int = 500, overlap: int = 50):
    """Split long documents into overlapping chunks"""
    
    words = document.split()
    chunks = []
    
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    
    return chunks
```

### 4. Multi-turn Conversation
Maintain conversation context:
```python
class ConversationRAG:
    def __init__(self):
        self.conversation_history = []
    
    def answer_with_context(self, query: str):
        """Answer considering conversation history"""
        
        # Include previous questions/answers as context
        conversation_context = "\n".join([
            f"Previous Q: {item['query']}\nA: {item['answer']}"
            for item in self.conversation_history[-3:]  # Last 3 exchanges
        ])
        
        # Modify prompt to include conversation context
        enhanced_query = f"Conversation history:\n{conversation_context}\n\nCurrent question: {query}"
        
        # Process normally with enhanced context
        result = self.answer_question(enhanced_query)
        
        # Store in history
        self.conversation_history.append({
            'query': query,
            'answer': result['answer']
        })
        
        return result
```

## Performance Optimization

### 1. Embedding Caching
```python
class EmbeddingCache:
    def __init__(self):
        self.cache = {}
    
    def get_embedding(self, text: str):
        if text in self.cache:
            return self.cache[text]
        
        embedding = self.generate_embedding(text)
        self.cache[text] = embedding
        return embedding
```

### 2. Index Optimization
```python
# For large datasets, use approximate search
index = faiss.IndexIVFFlat(quantizer, d, nlist)
index.train(embeddings)
index.add(embeddings)
index.nprobe = 10  # Search 10 clusters
```

### 3. Batch Processing
```python
def batch_process_queries(self, queries: List[str], batch_size: int = 5):
    """Process multiple queries efficiently"""
    
    results = []
    for i in range(0, len(queries), batch_size):
        batch = queries[i:i + batch_size]
        batch_embeddings = self.generate_embeddings(batch)
        
        for query, embedding in zip(batch, batch_embeddings):
            # Process with pre-computed embedding
            result = self.search_with_embedding(embedding)
            results.append(result)
    
    return results
```

## Evaluation Metrics

### 1. Retrieval Metrics
- **Precision@K**: Relevant documents in top-K results
- **Recall@K**: Fraction of relevant documents retrieved
- **MRR (Mean Reciprocal Rank)**: Average 1/rank of first relevant result

### 2. Generation Metrics
- **BLEU Score**: N-gram overlap with reference answers
- **ROUGE Score**: Recall-oriented evaluation
- **Semantic Similarity**: Embedding similarity with ground truth

### 3. Banking-Specific Metrics
- **Policy Compliance**: Answers align with banking regulations
- **Completeness**: All required information included
- **Accuracy**: Factual correctness of rates, requirements, etc.

## Deployment Considerations

### 1. Security
- Encrypt embeddings and indices
- Implement access controls
- Audit trail for sensitive queries
- PII detection and masking

### 2. Scalability
- Distributed vector search (e.g., Pinecone, Weaviate)
- Load balancing for API calls
- Caching strategies for frequent queries
- Horizontal scaling of retrieval services

### 3. Monitoring
- Query performance metrics
- Retrieval quality scores
- Response time monitoring
- User satisfaction feedback

This comprehensive RAG system provides accurate, contextual answers for banking and financial services, combining the power of semantic search with large language models for enhanced customer support.
