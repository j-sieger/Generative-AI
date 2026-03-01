import os
from dotenv import load_dotenv
from typing import Annotated, Literal, List, Optional
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_ibm import ChatWatsonx
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from pydantic import BaseModel, Field
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()

# --- Configuration ---
WATSONX_APIKEY = os.getenv('WATSONX_APIKEY', None)
WATSONX_PROJECT_ID = os.getenv('WATSONX_PROJECT_ID', None)
URL = os.getenv("WATSONX_URL","https://us-south.ml.cloud.ibm.com")

llm = ChatWatsonx(
    model_id="meta-llama/llama-3-3-70b-instruct",
    url = URL,
    apikey = WATSONX_APIKEY,
    project_id = WATSONX_PROJECT_ID,
)

# --- Mock Data ---
mock_research_data = {
    "Apple": {
        "recent_news": "Launched Vision Pro, expanding services revenue",
        "stock_info": "Trading at $195, up 45% YTD",
        "key_developments": "AI integration across product line"
    },
    "Tesla": {
        "recent_news": "Cybertruck deliveries ramping up",
        "stock_info": "Trading at $242, volatile quarter",
        "key_developments": "FSD v12 rollout, energy storage growth"
    }
}

# --- State Definition ---
class AgentState(BaseModel):
    messages: Annotated[List, add_messages]
    clarity_status: Optional[Literal["clear", "needs_clarification"]] = None
    research_findings: Optional[str] = None
    confidence_score: float = 0.0
    validation_result: Optional[Literal["sufficient", "insufficient"]] = None
    attempts: int = 0
    current_company: Optional[str] = None # To track context

# --- Agent 1: Clarity Agent ---
def clarity_agent(state: AgentState):
    """Analyzes if the user's query is clear and specific using LLM knowledge."""
    last_message = state.messages[-1]
    query = last_message.content
    current_context = state.current_company
    
    # Prompt the LLM to identify the company and verify if it's well-known
    prompt = f"""
    Analyze the following user query: "{query}"
    
    Current context company: {current_context if current_context else "None"}
    
    Task:
    1. Identify if the user is asking about a specific company.
    2. If yes, determine if it is a well-known public company or a major entity.
    3. If the query is vague (e.g., "what about the other one?") and no context exists, mark as unclear.
    4. If the company is obscure or made up, mark as unclear.
    
    Output strictly in JSON format without markdown backticks:
    {{
        "company_name": "Name of company" or null,
        "is_well_known": true/false,
        "is_clear": true/false,
        "reason": "explanation"
    }}
    """
    
    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        content = response.content.strip()
        
        # Robust JSON extraction
        start_idx = content.find('{')
        end_idx = content.rfind('}')
        
        if start_idx != -1 and end_idx != -1:
             content = content[start_idx:end_idx+1]
        
        import json
        result = json.loads(content)
        
        is_clear = result.get("is_clear", False)
        company_name = result.get("company_name")
        is_well_known = result.get("is_well_known", False)
        
        if is_clear and company_name and is_well_known:
            return {"clarity_status": "clear", "current_company": company_name}
        elif is_clear and current_context:
            # Query is clear about context (e.g. "stock price")
            return {"clarity_status": "clear"}
        else:
            return {"clarity_status": "needs_clarification"}
            
    except Exception as e:
        print(f"Error in clarity agent: {e}")
        return {"clarity_status": "needs_clarification"}

# --- Agent 2: Research Agent ---
def research_agent(state: AgentState):
    """Searches for company information based on the query."""
    company = state.current_company
    if not company or company not in mock_research_data:
        # Fallback if somehow we got here without valid company or company not in mock data
        # For this exercise, we assume "clear" status guarantees a valid company or we handle it gracefully
        return {
            "research_findings": f"No data found for {company}.",
            "confidence_score": 0.0,
            "attempts": state.attempts + 1
        }
    
    data = mock_research_data[company]
    # Simulate extracting relevant info based on query
    # In a real app, this would use an LLM or vector store to find specific info
    # For now, we return all info as 'search results'
    findings = f"Research for {company}:\n"
    findings += f"- News: {data['recent_news']}\n"
    findings += f"- Stock: {data['stock_info']}\n"
    findings += f"- Developments: {data['key_developments']}"
    
    # Simple confidence logic for mock
    confidence = 8.0 # Mock high confidence for valid data
    
    return {
        "research_findings": findings,
        "confidence_score": confidence,
        "attempts": state.attempts + 1
    }

# --- Agent 3: Validator Agent ---
def validator_agent(state: AgentState):
    """Reviews research quality and completeness."""
    # In a real scenario, LLM checks if findings answer the specific user query.
    # Here, we'll use a simple mock logic or LLM call. Let's use LLM for fun.
    
    # We invoke LLM to check if findings are sufficient for the last user message
    user_query = state.messages[-1].content
    findings = state.research_findings
    
    system_msg = SystemMessage(content="You are a validator. Check if the research findings are sufficient to answer the user's query. Reply valid or invalid.")
    human_msg = HumanMessage(content=f"Query: {user_query}\nFindings: {findings}")
    
    # For speed/simplicity in this specific mock exercise, we can just say 'sufficient' if findings are not empty
    # But let's respect the architecture.
    validation = "sufficient" if findings and "No data found" not in findings else "insufficient"
    
    return {"validation_result": validation}


# --- Agent 4: Synthesis Agent ---
def synthesis_agent(state: AgentState):
    """Creates a coherent summary."""
    user_query = state.messages[-1].content
    findings = state.research_findings
    
    prompt = f"""
    You are a helpful research assistant. 
    User asked: {user_query}
    
    Research findings:
    {findings}
    
    Please provide a concise answer to the user.
    """
    
    response = llm.invoke([HumanMessage(content=prompt)])
    return {"messages": [response]} # Add to conversation history


# --- Routing Logic ---

def route_clarity(state: AgentState):
    if state.clarity_status == "needs_clarification":
        return "clarification_interrupt"
    return "research_agent"

def route_research(state: AgentState):
    if state.confidence_score < 6:
        return "validator_agent"
    return "synthesis_agent" # Instructions say >= 6 goes to Synthesis directly, skipping validator? Wait.
    # Re-reading prompt: "ROUTES TO: Validator Agent (if confidence < 6) OR Synthesis Agent (if confidence >= 6)"
    # PROMPT ALSO SAYS: "Validator Agent... ROUTES TO: Research Agent ... OR Synthesis Agent"
    # So if confidence is high, we skip validator? The prompt implies that.
    # However, usually Validator checks ALL research. But I will follow the specific instruction for Research Agent routing.

def route_validator(state: AgentState):
    if state.validation_result == "insufficient" and state.attempts < 3:
        return "research_agent"
    return "synthesis_agent"

# --- Interrupt / Human Interaction ---
def clarification_interrupt(state: AgentState):
    # This node handles the case where clarification is needed.
    # We send a message to the user asking for clarification.
    msg = AIMessage(content="I'm not sure which company you're asking about. Could you please specify (e.g., 'Apple' or 'Tesla')?")
    return {"messages": [msg], "attempts": 0} # Reset attempts for new query?
    # We return to END, but with a message. The next user input will restart the flow.

# --- Graph Construction ---
workflow = StateGraph(AgentState)

workflow.add_node("clarity_agent", clarity_agent)
workflow.add_node("research_agent", research_agent)
workflow.add_node("validator_agent", validator_agent)
workflow.add_node("synthesis_agent", synthesis_agent)
workflow.add_node("clarification_interrupt", clarification_interrupt)

workflow.add_edge(START, "clarity_agent")

workflow.add_conditional_edges(
    "clarity_agent",
    route_clarity,
    {
        "clarification_interrupt": "clarification_interrupt",
        "research_agent": "research_agent"
    }
)

workflow.add_edge("clarification_interrupt", END) 
# After asking for clarification, we end this turn. User replies next.

workflow.add_conditional_edges(
    "research_agent",
    route_research,
    {
        "validator_agent": "validator_agent",
        "synthesis_agent": "synthesis_agent"
    }
)

workflow.add_conditional_edges(
    "validator_agent",
    route_validator,
    {
        "research_agent": "research_agent",
        "synthesis_agent": "synthesis_agent"
    }
)

workflow.add_edge("synthesis_agent", END)

# Compile with checkpointer for conversation memory
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)


# --- Execution Loop (CLI) ---
if __name__ == "__main__":
    import uuid
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    
    print("Welcome to the Multi-Agent Research Assistant! (Type 'quit' to exit)")
    print(f"Session ID: {thread_id}")
    
    while True:
        user_input = input("\nUser: ")
        if user_input.lower() in ["quit", "exit"]:
            break
        
        # We append the user message to the state
        # The graph will pick it up from 'messages'
        events = app.stream(
            {"messages": [HumanMessage(content=user_input)]},
            config=config,
            stream_mode="values"
        )
        
        for event in events:
            if "messages" in event:
                # Print the last message if it's from AI (to avoid re-printing user input if it's echoed)
                last_msg = event["messages"][-1]
                # We only want to print the FINAL response from the assistant in this loop,
                # but 'stream' yields state updates.
                # A simple way is to check if loop finished and print final.
                # But for 'values' mode, it yields the state at each step.
                pass

        # Get final state to print the actual response
        snapshot = app.get_state(config)
        if snapshot.values and snapshot.values['messages']:
            last_msg = snapshot.values['messages'][-1]
            if isinstance(last_msg, AIMessage):
                print(f"Assistant: {last_msg.content}")