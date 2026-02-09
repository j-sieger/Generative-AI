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

class MessageClassifier(BaseModel):
    #Literal tells that variable message_type is going to either one of those 2 options
    message_type: Literal["emotional", "logical"] = Field(
        ...,
        description="Classify if the message requires an emotional (therapist) or logical response."
    )

#For adding the messages from human and llm to state
class State(TypedDict):
    messages: Annotated[list, add_messages]
    message_type: str|None


def classify_message(state:State):
    #Get the last message for classifying
    last_message = state["messages"][-1]
    classifier_llm = llm.with_structured_output(MessageClassifier)

    result = classifier_llm.invoke([
        {
            "role": "system",
            "content": """Classify the user message as either:
            - 'emotional': if it asks for emotional support, therapy, deals with feelings, or personal problems
            - 'logical': if it asks for facts, information, logical analysis, or practical solutions
            """
        },
        {"role": "user", "content": last_message.content}
    ])
    # print("I am in classifier: ",result)
    return {"message_type": result.message_type}

def router(state:State):
    message_type = state.get("message_type","logical")
    if message_type == "emotional":
        return {"next":"therapist"}
    # print("I am in router: ",message_type)
    return{"next":"logical"}
    
def therapist_agent(state:State):
    last_message = state['messages'][-1]
    messages = [
        {"role": "system",
         "content": """You are a compassionate therapist. Focus on the emotional aspects of the user's message.
                        Show empathy, validate their feelings, and help them process their emotions.
                        Ask thoughtful questions to help them explore their feelings more deeply.
                        Avoid giving logical solutions unless explicitly asked."""
         },
        {
            "role": "user",
            "content": last_message.content
        }        
    ]
    reply = llm.invoke(messages)
    # print("I am in terapist agent: ",reply)
    return {"messages":[{"role":"assistant","content":reply.content}]}

def logical_agent(state:State):
    last_message = state["messages"][-1]

    messages = [
        {"role": "system",
         "content": """You are a purely logical assistant. Focus only on facts and information.
            Provide clear, concise answers based on logic and evidence.
            Do not address emotions or provide emotional support.
            Be direct and straightforward in your responses."""
         },
        {
            "role": "user",
            "content": last_message.content
        }
    ]
    reply = llm.invoke(messages)
    # print("I am in logical agent: ",reply)
    return {"messages": [{"role": "assistant", "content": reply.content}]}


graph_builder = StateGraph(State)

graph_builder.add_node("classifier",classify_message)
graph_builder.add_node("router",router)
graph_builder.add_node("logical_ag",logical_agent)
graph_builder.add_node("therapist_ag",therapist_agent)

graph_builder.add_edge(START,"classifier")
graph_builder.add_edge("classifier","router")
graph_builder.add_conditional_edges("router",
                                    lambda state: state.get("next"),
                                    {"therapist":"therapist_ag","logical":"logical_ag"}
                                    )
graph_builder.add_edge("therapist_ag",END)
graph_builder.add_edge("logical_ag",END)

graph = graph_builder.compile()


def run_chatbot():
    state = {"messages":[], "message_type":None}
    while True:
        user_input = input("Enter Message:")
        if user_input=="exit":
            print("Bye")
            break
        #Merge userinput to existing list of message.if not merge it with empty list []
        #We can maintain the history
        state["messages"] = state.get("messages", []) + [
            {"role": "user", "content": user_input}
        ]
        
        state = graph.invoke(state)
        #state = graph.invoke({"messages":{"role":"user","content":user_input}})
        if state.get("messages") and len(state["messages"]) > 0:
            
            last_message = state["messages"][-1]
            print(f"Assistant: {last_message.content}")


if __name__=='__main__':

    run_chatbot()
    """ Test Messages:
        Emotional = Hey, I am really sad today.
        Logical: I need advice on buying house.
    """



    
