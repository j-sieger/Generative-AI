
import sys
import os

# Add current directory to path so we can import multiagent
sys.path.append(os.getcwd())

from multiagent import app
from langchain_core.messages import HumanMessage
import uuid

def run_test():
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    
    print(f"=== Starting Test Session {thread_id} ===")
    
    # Test 1: Direct Query
    query1 = "Tell me about Apple."
    print(f"\nUser: {query1}")
    result1 = app.invoke({"messages": [HumanMessage(content=query1)]}, config=config)
    print("Final Result 1:", result1['messages'][-1].content)
    
    # Test 2: Vague Query -> Clarification -> Specific
    query2 = "What about the other company?"
    print(f"\nUser: {query2}")
    result2 = app.invoke({"messages": [HumanMessage(content=query2)]}, config=config)
    print("Final Result 2:", result2['messages'][-1].content)
    
    query3 = "Tesla"
    print(f"\nUser: {query3}")
    result3 = app.invoke({"messages": [HumanMessage(content=query3)]}, config=config)
    print("Final Result 3:", result3['messages'][-1].content)

    # Test 3: Follow up with context
    query4 = "What is the stock price?"
    print(f"\nUser: {query4}")
    result4 = app.invoke({"messages": [HumanMessage(content=query4)]}, config=config)
    print("Final Result 4:", result4['messages'][-1].content)

    # Test 4: Well-known company not in mock data (Microsoft)
    query5 = "Microsoft"
    print(f"\nUser: {query5}")
    result5 = app.invoke({"messages": [HumanMessage(content=query5)]}, config=config)
    print("Final Result 5:", result5['messages'][-1].content)
    
    # Test 5: Made up company
    query6 = "BashaFlyingCars Inc."
    print(f"\nUser: {query6}")
    result6 = app.invoke({"messages": [HumanMessage(content=query6)]}, config=config)
    print("Final Result 6:", result6['messages'][-1].content)

if __name__ == "__main__":
    run_test()
