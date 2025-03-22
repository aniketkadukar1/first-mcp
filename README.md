# Documentation Search MCP

A Cursor MCP server that allows you to search documentation from popular AI/ML libraries directly within your IDE. Currently supports:
- LangChain
- LlamaIndex
- OpenAI

## Features

- Quick documentation search across multiple libraries
- Integration with Cursor IDE
- Real-time search results using Tavily API
- Asynchronous processing for better performance

## Prerequisites

- [Cursor IDE](https://cursor.sh/) --> Can be any other client too
- [uv](https://github.com/astral-sh/uv) - Fast Python package installer
- Python 3.11+
- Tavily API key

## Setup

1. Clone the repository:
```bash
git clone <your-repo-url>
cd first-mcp
```

2. Install dependencies using uv:
```bash
uv pip install -r requirements.txt
```

3. Create a `.env` file in the project root and add your Tavily API key:
```
TAVILY_API_KEY=your_api_key_here
```

4. Configure Cursor MCP: [If you are using cursor as a client]
   - Open or create `C:\Users\<username>\.cursor\mcp.json`
   - Add the following configuration:
```json
{
    "mcpServers": {
        "documemtation": {
            "command": "<directory_where_uv_is_installed>/uv",
            "args": [
                "--directory",
                "<project_directory>",
                "run",
                "main.py"
            ]
        }
    }
    
```

## Usage

1. In Cursor IDE, use the command palette (Ctrl/Cmd + P)
2. Type `get_docs` followed by your query and library name
3. Example queries:
   - `get_docs "how to use LLMs" "langchain"`
   - `get_docs "vector stores" "llama-index"`
   - `get_docs "chat completions" "openai"`

## Project Structure

- `main.py` - Main server implementation
- `mcp.json` - MCP server configuration
- `.env` - Environment variables (API keys)

## Dependencies

- FastMCP - MCP server implementation
- python-dotenv - Environment variable management
- requests - HTTP client
- httpx - Async HTTP client
- beautifulsoup4 - HTML parsing
