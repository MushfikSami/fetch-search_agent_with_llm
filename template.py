from langchain_core.prompts import PromptTemplate


research_template = """Answer the question step by step using the tools.

Question: {input}

TOOLS ({tool_names}):

Use this exact format:
Thought: [your reasoning]
Action: [tool name]  
Action Input: [tool input]
Observation: [tool output]
... repeat ...
Thought: I have enough info
Final Answer: [your answer]

Begin!

{agent_scratchpad}"""

custom_prompt = PromptTemplate.from_template(research_template)

print("✅ Custom prompt ready")
