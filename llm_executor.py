from langchain_classic.agents import AgentExecutor, create_react_agent
from langchain_openai import ChatOpenAI
from tools import VLLM_API_KEY, VLLM_MODEL_NAME, VLLM_URL,tools
from langchain_classic import hub
llm = ChatOpenAI(
    model=VLLM_MODEL_NAME,
    base_url=VLLM_URL,
    api_key=VLLM_API_KEY,
    temperature=0.7
)

# Pull official ReAct prompt (v1.0.x standard)
react_prompt = hub.pull("hwchase17/react")

# Create modern ReAct agent
agent = create_react_agent(llm, tools, react_prompt)

# v1.0.x Executor
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=5
)

print("✅ v1.0.x ReAct agent ready!")
print("Usage: agent_executor.invoke({\"input\": \"query\"})")
