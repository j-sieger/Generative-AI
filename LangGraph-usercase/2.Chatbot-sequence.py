import os
from dotenv import load_dotenv
from typing import Annotated, Literal
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from langchain_ibm import ChatWatsonx
from pydantic import BaseModel, Field
from typing_extensions import TypedDict

load_dotenv()

WATSONX_APIKEY = os.getenv('WATSONX_APIKEY', None)
WATSONX_PROJECT_ID = os.getenv('WATSONX_PROJECT_ID', None)
URL = os.getenv("WATSONX_URL","https://us-south.ml.cloud.ibm.com")

llm = ChatWatsonx(
    model_id="meta-llama/llama-3-3-70b-instruct",
    url = URL,
    apikey = WATSONX_APIKEY,
    project_id = WATSONX_PROJECT_ID,
)

#For adding the messages from human and llm to state
class State(TypedDict):
    messages: Annotated[list, add_messages]

graph_builder = StateGraph(State)


def chatbot(state:State):
    print("Messages in state:",state['messages'])
    
    return {"messages":[llm.invoke(state["messages"])]}


graph_builder.add_node("cb",chatbot)
graph_builder.add_edge(START,"cb")
graph_builder.add_edge("cb",END)

graph = graph_builder.compile()

user_input = input("Enter Message:")
state = graph.invoke({"messages":{"role":"user","content":user_input}
                            })
print("Updates mesages in State:",state["messages"])
print(state['messages'][-1].content)



    
