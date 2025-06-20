# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository implements an MCP (Model Context Protocol) agent proof of concept with the following architecture:
- Frontend (React/Vue) → LangChain Agent → MCP Tools → RAG microservice
- Chat-based UI supporting multimodal inputs (text and images)
- RAG microservice integration via `/query` endpoint at `http://localhost:8000`

## Key Architecture Components

### MCP-RAG Integration
- Custom MCP tool (`MCPRAGTool`) interfaces with RAG microservice
- RAG endpoint returns structured responses with sources, similarity scores, and metadata
- Supports complex query composition with metadata, text, and image sections

### Query Structure
User queries are composed of multiple elements in Markdown format:
- Metadata section (document title, job_id)  
- Text section (user query text)
- Image section (filename, base64 encoded image)

### RAG Response Format
The RAG microservice returns JSON responses containing:
- `response`: Main response text
- `response_sources`: Array of source documents with node_id, score, job_id, title, date, speakers
- `similarity_score`: Embedding and text similarity scores
- `user_query`: Original query text

## Technology Stack
- Backend: Python with LangChain agent framework
- Frontend: React or Vue.js (component-based chat UI)
- Protocol: MCP (Model Context Protocol)
- RAG Service: Microservice architecture with REST API

## Development Notes
- The codebase uses Python-style .gitignore suggesting Python backend implementation
- Frontend UI/UX should be modular and easily adaptable per scenario
- Multimodal LLM support required for text and image processing
- MCP protocol compliance is essential for tool definitions and integrations
- Currently the project root directory is set to `~/repo/mcp-agent-poc`, but you should notify me to change here if it seems not correct

## Testing Requirements

### Dummy RAG Microservice
A dummy RAG microservice should be implemented to properly test the MCP agent:
- Implement a simple REST API server with `/query` endpoint on `http://localhost:8000`
- Return mock responses matching the expected JSON structure with realistic test data
- Support the full query structure (metadata, text, and image sections)
- Include sample documents with varied node_ids, job_ids, titles, dates, and speakers
- Provide configurable similarity scores for testing different scenarios
- This allows end-to-end testing of the MCP agent without requiring a full RAG implementation