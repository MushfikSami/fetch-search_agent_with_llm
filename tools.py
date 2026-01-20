# =============================================================================
# LangChain v1.0.x - Latest Official Release
# WebSurfX + VLLM Single Agent (Modern API)
# =============================================================================

# Cell 1: v1.0.x IMPORTS
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_classic.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate
from langchain_classic import hub
import requests
from bs4 import BeautifulSoup
import re
import time

print("✅ LangChain v1.0.x imports")

# Cell 2: TOOLS (v1.0.x Optimized)

WEBSURFX_URL = "http://0.0.0.0:8080"
VLLM_URL = "http://127.0.0.1:5000/v1"
VLLM_API_KEY = "no-key"
VLLM_MODEL_NAME = "cpatonn/Qwen3-30B-A3B-Thinking-2507-AWQ-4bit"
@tool
def search_web(query: str) -> str:
    """WebSurf-X search tool"""
    try:
        # WebSurf-X returns HTML even with ?format=json
        # Extract results from HTML structure
        resp = requests.get("http://localhost:8080/search", 
                           params={"q": query}, timeout=12)
        
        soup = BeautifulSoup(resp.text, "html.parser")
        
        # WebSurf-X result selectors (from your HTML)
        results = soup.select(".result") or soup.select("article") or soup.select(".entry")
        
        if not results:
            # Fallback: all links
            results = soup.select("a[href*='http']")[:10]
        
        output = f"WebSurf-X Results for '{query}':\n\n"
        for i, result in enumerate(results[:8], 1):
            title_elem = result.select_one("h3, .title, h2, h1") or result
            link_elem = result.select_one("a")
            
            title = title_elem.get_text(strip=True)[:80]
            url = link_elem.get("href") if link_elem else ""
            
            if url and title and "http" in url:
                snippet = result.get_text(strip=True)[:120]
                output += f"{i}. **{title}**\n"
                output += f"   {url}\n"
                output += f"   {snippet}...\n\n"
        
        return output if len(output) > 100 else "No results found"
        
    except Exception as e:
        return f"[WebSurf-X error: {str(e)}]"

@tool
def get_content(urls: list[str]) -> str:
    """Extract content from URLs"""
    content = ""
    for url in urls[:3]:
        try:
            r = requests.get(url, timeout=10)
            soup = BeautifulSoup(r.content, "html.parser")
            
            # Clean content
            for tag in soup(["script", "style", "nav", "footer"]):
                tag.decompose()
            
            text = soup.get_text(separator=" ", strip=True)[:2500]
            title = soup.title.string if soup.title else url.split("/")[-1]
            
            content += f"\n## {title}\n\n{text[:600]}...\n\n"
            time.sleep(0.5)
        except Exception:
            continue
    
    return content or "No content retrieved"

@tool
def summarize_content(text: str, query: str) -> str:
    """Summarize content using VLLM"""
    from openai import OpenAI
    
    client = OpenAI(base_url=VLLM_URL, api_key=VLLM_API_KEY)
    
    prompt = f"""Original query: "{query}"

Summarize the most relevant information from this content:

{text[:4000]}

Provide a concise, accurate summary:"""
    
    try:
        response = client.chat.completions.create(
            model=VLLM_MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=500
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Summarization failed: {str(e)}"

tools = [search_web, get_content, summarize_content]
print(f"✅ {len(tools)} v1.0.x tools loaded")




