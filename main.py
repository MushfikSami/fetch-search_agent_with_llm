from llm_executor import agent_executor

V10_AGENT = agent_executor

def research(query: str):
    """One-line research"""
    return V10_AGENT.invoke({"input": query})

def batch_research(queries: list[str]):
    """Batch research"""
    return [research(q) for q in queries]

query="what is the capital of France?"
agent_executor.invoke({"input": query})