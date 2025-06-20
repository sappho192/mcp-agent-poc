from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import uuid
from datetime import datetime
import uvicorn


app = FastAPI(title="Dummy RAG Microservice", version="1.0.0")


class QueryRequest(BaseModel):
    query: str


class ResponseSource(BaseModel):
    node_id: str
    score: float
    job_id: str
    title: str
    date: str
    speakers: str


class SimilarityScore(BaseModel):
    type: str
    score: float


class RAGResponse(BaseModel):
    response: str
    response_sources: List[ResponseSource]
    similarity_score: List[SimilarityScore]
    user_query: str


# Mock data for testing
MOCK_DOCUMENTS = [
    {
        "node_id": "1b37a413-6063-43a0-8261-4ddb610f1a20",
        "job_id": "3bf38964-7858-4352-94c8-c96bd89550ed",
        "title": "Machine Learning Best Practices",
        "date": "2024-10-10 11:00:00",
        "speakers": "John Doe, Jane Smith",
        "content": "machine learning algorithms data science neural networks"
    },
    {
        "node_id": "2c48b524-7174-54b1-9372-5eec721f2b31",
        "job_id": "4cg49a75-8969-5463-a5d9-d97ce8a661fe",
        "title": "Python Development Guide",
        "date": "2024-09-15 14:30:00",
        "speakers": "Alice Johnson, Bob Wilson",
        "content": "python programming software development web frameworks"
    },
    {
        "node_id": "3d59c635-8285-65c2-a483-6ffd832g3c42",
        "job_id": "5dh5ab86-9a7a-6574-b6ea-ea8df9b772gf",
        "title": "Database Architecture",
        "date": "2024-11-20 09:15:00", 
        "speakers": "Charlie Brown, Diana Prince",
        "content": "database design sql nosql data modeling performance"
    }
]


def calculate_similarity(query: str, content: str) -> float:
    """Simple keyword-based similarity calculation"""
    query_words = set(query.lower().split())
    content_words = set(content.lower().split())
    intersection = query_words.intersection(content_words)
    if not query_words:
        return 0.0
    return len(intersection) / len(query_words)


@app.post("/query", response_model=RAGResponse)
async def query_rag(request: QueryRequest):
    """Process RAG query and return mock response with realistic data"""
    
    query = request.query.lower()
    
    # Calculate similarity scores for each document
    scored_docs = []
    for doc in MOCK_DOCUMENTS:
        similarity = calculate_similarity(query, doc["content"])
        if similarity > 0:  # Only include documents with some relevance
            scored_docs.append({
                **doc,
                "relevance_score": similarity * 10  # Scale to 0-10 range
            })
    
    # Sort by relevance and take top 3
    scored_docs.sort(key=lambda x: x["relevance_score"], reverse=True)
    top_docs = scored_docs[:3]
    
    # Generate response based on query content
    if "machine learning" in query or "ml" in query:
        response_text = "Machine learning involves training algorithms on data to make predictions or decisions. Key practices include data preprocessing, model selection, and performance evaluation."
    elif "python" in query or "programming" in query:
        response_text = "Python is a versatile programming language widely used for web development, data science, and automation. It offers clean syntax and extensive libraries."
    elif "database" in query or "sql" in query:
        response_text = "Database architecture involves designing efficient data storage and retrieval systems. Key considerations include normalization, indexing, and query optimization."
    else:
        response_text = f"Based on your query about '{request.query}', here are some relevant insights from our knowledge base."
    
    # Create response sources
    response_sources = [
        ResponseSource(
            node_id=doc["node_id"],
            score=doc["relevance_score"],
            job_id=doc["job_id"],
            title=doc["title"],
            date=doc["date"],
            speakers=doc["speakers"]
        )
        for doc in top_docs
    ]
    
    # Calculate similarity scores
    avg_similarity = sum(doc["relevance_score"] for doc in top_docs) / len(top_docs) if top_docs else 0
    similarity_scores = [
        SimilarityScore(type="embedding", score=avg_similarity / 10),
        SimilarityScore(type="text", score=(avg_similarity / 10) * 1.1)  # Slightly higher text score
    ]
    
    return RAGResponse(
        response=response_text,
        response_sources=response_sources,
        similarity_score=similarity_scores,
        user_query=request.query
    )


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)