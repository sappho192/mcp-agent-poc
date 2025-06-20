from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory
from langchain.schema import BaseMessage
from typing import Dict, Any, List
import os
from dotenv import load_dotenv

from backend.tools.mcp_rag_tool import MCPRAGTool

load_dotenv()


class MCPAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.7,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        self.tools = [MCPRAGTool()]
        
        self.memory = ConversationBufferWindowMemory(
            memory_key="chat_history",
            return_messages=True,
            k=10
        )
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an AI assistant with access to a RAG (Retrieval-Augmented Generation) system.
            
Your capabilities:
- Query knowledge bases using the RAG tool to find relevant information
- Process multimodal inputs including text and images
- Provide comprehensive responses based on retrieved documents
- Cite sources when providing information

When users ask questions:
1. Use the mcp_rag_query tool to search for relevant information
2. Synthesize the retrieved information with your knowledge
3. Provide clear, helpful responses
4. Include source references when available

Handle complex queries that may include:
- Metadata sections (document titles, job IDs)
- Text queries
- Image descriptions or references

Always strive to be helpful, accurate, and cite your sources."""),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        self.agent = create_openai_functions_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt
        )
        
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            memory=self.memory,
            verbose=True,
            handle_parsing_errors=True
        )
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """Process a user query and return the agent's response"""
        try:
            result = self.agent_executor.invoke({"input": query})
            return {
                "response": result["output"],
                "success": True
            }
        except Exception as e:
            return {
                "response": f"I encountered an error processing your request: {str(e)}",
                "success": False,
                "error": str(e)
            }
    
    def reset_memory(self):
        """Clear the conversation memory"""
        self.memory.clear()