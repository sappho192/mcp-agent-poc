# mcp-agent-poc

## Description

This is a proof of concept for the MCP agent.

## Main features

The PoC implements an AI agent fulfilling following requirements:

1. AI agent should be MCP-based, or have ability to work with MCP
2. The microservice-based RAG engine which provides query endpoint like `/query` can be attached to the agent
3. The basic demo frontend UI will be chat-based like ChatGPT or Claude, but the frontend UI/UX can be easily changed per scenario
4. The above chat-based UI should accept multimodal inputs like text or image inside chatbox since multimodal LLM will be used in the backend

## Architecture

Frontend (React) -> LangChain Agent -> MCP Tools -> RAG microservice

## Setup and Installation

### Prerequisites
- Python 3.11+
- Node.js 18+
- PDM (Python Dependency Manager)
- OpenAI API Key

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd mcp-agent-poc
   ```

2. **Set up Python environment:**
   ```bash
   # PDM should already be initialized with dependencies
   pdm install
   ```

3. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

4. **Set up frontend:**
   ```bash
   cd frontend
   npm install
   cd ..
   ```

## Running the Application

The application consists of three components that need to be started separately:

### 1. Start the RAG Microservice (Port 8000)
```bash
python start_rag_service.py
```

### 2. Start the MCP Agent Backend (Port 8001)
```bash
python start_agent.py
```

### 3. Start the Frontend (Port 3000)
```bash
# Option 1: Use the startup script
./start_frontend.sh

# Option 2: Manual start
cd frontend
npm start
```

The application will be available at: http://localhost:3000

## Testing

1. Open the frontend at http://localhost:3000
2. Try different types of queries:
   - Simple text: "What is machine learning?"
   - With metadata: "title: ML Guide job_id: 123 What are best practices?"
   - Upload an image and ask questions about it

## Implementation

- Use LangChain's agent framework as the core
- Implement MCP protocol support via custom tools/integrations
- Create MCP-compatible tool definitions for the RAG microservice
- Build modular frontend with component-based chat UI

## Key Components:

### Custom MCP tool for RAG
```Python
class MCPRAGTool:
    def call_rag_endpoint(self, query: str):
        response = requests.post("http://localhost:8000/query", json={"query": query})
        return response.json()
```
### Example response from RAG microservice
```json
{
  "response": "Response text of user query",
  "response_sources": [
    {
      "node_id": "1b37a413-6063-43a0-8261-4ddb610f1a20",
      "score": 7.927279949188232,
      "job_id": "3bf38964-7858-4352-94c8-c96bd89550ed",
      "title": "Title of document",
      "date": "2024-10-10 11:00:00",
      "speakers": "John Dow, Jane Smith"
    },
  ],
  "similarity_score": [
    {
      "type": "embedding",
      "score": 0.280217696584437
    },
    {
      "type": "text",
      "score": 0.29580398915498074
    }
  ],
  "user_query": "User query text"
}
```

### Example scenario from frontend page

User query can be composed of list of following elements:
- Metadata text (e.g. document title, job_id)
- Text query
- Image query

Above elements will be combined randomly to form a complete user query.
The example of complete user query is like below:

```Markdown
# Metadata section
## Document title
This is a title of document
## Job ID
3bf38964-7858-4352-94c8-c96bd89550ed

# Text section
## Query
User query text

# Image section
## Filename
This is a filename of image
## Base64
This is a base64 encoded image

# Text section
## Query
Another user query text
```

## Project Structure

```
mcp-agent-poc/
├── backend/
│   ├── agent/
│   │   └── langchain_agent.py    # Main LangChain agent
│   ├── tools/
│   │   └── mcp_rag_tool.py       # MCP RAG tool implementation
│   ├── rag_service/
│   │   └── dummy_rag.py          # Dummy RAG microservice
│   └── main.py                   # FastAPI backend server
├── frontend/                     # React frontend
│   ├── src/
│   │   ├── App.tsx              # Main chat interface
│   │   └── App.css              # Chat UI styles
│   └── package.json
├── start_rag_service.py          # RAG service startup script
├── start_agent.py                # Agent backend startup script
├── .env.example                  # Environment variables template
├── pyproject.toml               # Python dependencies
└── README.md
```

