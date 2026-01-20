from llm_executor import agent_executor

test_query = "President of USA"
print(f"\n🧪 v1.0.x Agent Test: {test_query}")
print("=" * 60)

result = agent_executor.invoke({"input": test_query})
print("\n✅ RESULT:")
print(result["output"])