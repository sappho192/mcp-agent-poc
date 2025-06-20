import requests
from typing import Dict, Any, List, Type
from langchain.tools import BaseTool
from pydantic import BaseModel, Field


class MCPRAGInput(BaseModel):
    query: str


class MCPRAGTool(BaseTool):
    name: str = "mcp_rag_query"
    description: str = "Query the RAG microservice to retrieve relevant documents and generate responses"
    args_schema: Type[BaseModel] = MCPRAGInput
    rag_endpoint: str = Field(default="http://localhost:8000/query")
    
    def _run(self, query: str) -> Dict[str, Any]:
        """Call the RAG endpoint with the provided query"""
        try:
            response = requests.post(
                self.rag_endpoint,
                json={"query": query},
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "error": f"Failed to query RAG service: {str(e)}",
                "response": "Unable to retrieve information from RAG service",
                "response_sources": [],
                "similarity_score": [],
                "user_query": query
            }
    
    async def _arun(self, query: str) -> Dict[str, Any]:
        """Async version of the run method"""
        return self._run(query)