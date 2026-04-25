# Fetch & Search Agent with LLM

A LangChain-based research agent that uses WebSurfX for web search and an LLM (via vLLM) to answer questions through a ReAct agent loop.

## Architecture

```
User Query → LangChain ReAct Agent → [WebSurfX Search] → LLM Summarize → Answer
```

The agent has three tools:
- **search_web** — queries WebSurfX for web results
- **get_content** — fetches and extracts text from URLs
- **summarize_content** — summarizes content via vLLM

## Quick Start

### 1. Start WebSurfX

```bash
docker compose up
```

This starts the WebSurfX search engine on port 8080 and optionally Redis for caching.

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Your LLM

Update the model endpoint in [tools.py](tools.py):

```python
VLLM_URL = "http://your-vllm-endpoint/v1"
VLLM_API_KEY = "your_api_key"
VLLM_MODEL_NAME = "your-model-name"
```

Or use [llm_executor.py](llm_executor.py) which configures the agent with these settings.

### 4. Run the Agent

**Interactive usage:**

```python
from main import research

result = research("What is quantum computing?")
print(result)
```

**Or run the test script:**

```bash
python test.py
```

**Or run directly:**

```bash
python main.py
```

## File Structure

| File | Purpose |
|------|---------|
| `main.py` | Entry point — exposes `research()` and `batch_research()` functions |
| `llm_executor.py` | Sets up the LangChain ReAct agent with tools |
| `tools.py` | Defines the three tools (search, fetch, summarize) |
| `template.py` | Custom ReAct prompt template |
| `test.py` | Quick test script |
| `docker-compose.yml` | WebSurfX + Redis container setup |
| `websurfx/config.lua` | WebSurfX configuration (port, search engines, safe search) |
| `websurfx/blocklist.txt` | Domain blocklist |
| `websurfx/allowlist.txt` | Domain allowlist |
| `requirements.txt` | Python dependencies |

## WebSurfX Configuration

Edit [websurfx/config.lua](websurfx/config.lua) to customize:
- **Safe search level** — set `safe_search` (0-4)
- **Search engines** — enable DuckDuckGo, Searx, etc.
- **Threads** — number of concurrent search threads
- **Rate limiting** — requests per time window

## Dependencies

- **LangChain v1.0.x** — agent framework
- **WebSurfX** — privacy-focused web search engine
- **vLLM** — fast LLM inference server
- **OpenAI SDK** — used to call vLLM-compatible API
