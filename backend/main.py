from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn
import os
from dotenv import load_dotenv

from backend.agent.langchain_agent import MCPAgent

load_dotenv()

app = FastAPI(title="MCP Agent API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React/Vue dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the MCP agent
agent = MCPAgent()


class ChatRequest(BaseModel):
    message: str
    reset_memory: Optional[bool] = False


class ChatResponse(BaseModel):
    response: str
    success: bool
    error: Optional[str] = None


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Process chat messages through the MCP agent"""
    
    if request.reset_memory:
        agent.reset_memory()
    
    try:
        result = agent.process_query(request.message)
        return ChatResponse(
            response=result["response"],
            success=result["success"],
            error=result.get("error")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent processing failed: {str(e)}")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "agent_initialized": agent is not None,
        "openai_key_configured": bool(os.getenv("OPENAI_API_KEY"))
    }


@app.post("/reset")
async def reset_conversation():
    """Reset the agent's conversation memory"""
    agent.reset_memory()
    return {"message": "Conversation memory reset successfully"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)