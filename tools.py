import os
import requests
from dotenv import load_dotenv
from langchain.tools import tool
from tavily import TavilyClient
from bs4 import BeautifulSoup


load_dotenv()


# =========================================================
# Tavily Client
# =========================================================

tavily = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)


# =========================================================
# Web Search Tool
# =========================================================

@tool
def web_search(query: str) -> str:
    """
    Search the web for recent and reliable information.

    The input must be a natural-language search query.
    Example: "latest developments in artificial intelligence"

    Returns search result titles, URLs, and snippets.
    """
    results = tavily.search(
        query=query,
        max_results=3
    )

    out = []

    for r in results.get("results", []):
        out.append(
            f"Title: {r['title']}\n"
            f"URL: {r['url']}\n"
            f"Snippet: {r['content'][:300]}"
        )

    return "\n\n".join(out)


# =========================================================
# URL Scraping Tool
# =========================================================

@tool
def scrap_url(url: str) -> str:
    """
    Scrape a webpage and return clean text from the
    given URL for deeper reading.
    """
    try:
        response = requests.get(
            url,
            timeout=8,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )
        response.raise_for_status()
        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )
        for tag in soup([
            "script",
            "style",
            "nav",
            "footer",
            "header",
            "aside",
            "form"
        ]):
            tag.decompose()
        text = soup.get_text(
            separator=" ",
            strip=True
        )
        if not text:
            return "No readable content found on this webpage."
        return text[:5000]
    except requests.exceptions.RequestException as e:
        return f"Could not scrape URL: {str(e)}"
    except Exception as e:
        return f"Unexpected error while scraping URL: {str(e)}"