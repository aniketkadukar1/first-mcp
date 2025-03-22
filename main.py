from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import requests
import httpx
from bs4 import BeautifulSoup

load_dotenv()

mcp = FastMCP("docs")

USER_AGENT = "docs-app/1.0"

TAVILY_URL = "https://api.tavily.com/search"

docs_urls = {
    "langchain": "https://python.langchain.com/docs",
    "llama-index": "https://docs.llamaindex.ai/en/stable",
    "openai": "https://platform.openai.com/docs",
}

async def search_web(query: str) -> dict | None:
    payload = {
    "query": query,
    "topic": "general",
    "search_depth": "basic",
    "chunks_per_source": 3,
    "max_results": 1,
    "time_range": None,
    "days": 3,
    "include_answer": True,
    "include_raw_content": False,
    "include_images": False,
    "include_image_descriptions": False,
    "include_domains": [],
    "exclude_domains": []
    }
    headers = {
        "Authorization": "Bearer <token>",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.request("POST", TAVILY_URL , json=payload, headers=headers)
        return response.json()
    except httpx.TimeoutException:
        return {"results": []}


async def fetch_url(url: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=30)
            soup = BeautifulSoup(response.text, "html.parser")
            text = soup.get_text()
            return text
        except httpx.TimeoutException:
            return "Timeout error"

@mcp.tool()
async def get_docs(query: str, library: str):
    """
    Search the docs for a given query and library.
    Supports langchain, llama-index, openai.

    Args:
        query: The query to search for (e.g. "Chroma DB").
        library: The library to search in (e.g. "langchain").
    
    Returns:
        Text from the docs.
    """

    if library not in docs_urls:
        raise ValueError(f"Library {library} not supported")

    query = f"site:{docs_urls[library]} {query}"

    results = await search_web(query)

    if len(results["results"]) == 0:
        return "No results found"
    
    text = ""
    for result in results["results"]:
        text += await fetch_url(result["url"])
    return text


if __name__ == "__main__":
    mcp.run(transport="stdio")
