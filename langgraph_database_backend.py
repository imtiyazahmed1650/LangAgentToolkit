from langgraph.graph import StateGraph,START,END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph.message import add_messages
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langgraph.checkpoint.sqlite import SqliteSaver
from dotenv import load_dotenv
import sqlite3
import os


load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("Groq API Key missing in .env file")

class ChatState(TypedDict):
    messages : Annotated[list[BaseMessage], add_messages]

model = ChatGroq(
    groq_api_key=GROQ_API_KEY, 
    model_name="llama-3.3-70b-versatile", 
    temperature=0.3
)

def ChatNode(state : ChatState) -> dict:
    """Chatbot node: takes messages from state and generates reply"""
    response = model.invoke(state["messages"])
    return {"messages":  [response]}


conn = sqlite3.connect(database='chatbot.db', check_same_thread=False)
checkpointer = SqliteSaver(conn=conn)

graph = StateGraph(ChatState)
graph.add_node("chatbot", ChatNode)
graph.add_edge(START, "chatbot")
graph.add_edge("chatbot", END)
 

chatbot = graph.compile(checkpointer=checkpointer)

def retrieve_all_threads():
    seen_ids = set()
    all_threads = []

    for i, checkpoint in enumerate(checkpointer.list(None), start=1):
        thread_id = checkpoint.config['configurable']['thread_id']

        if thread_id not in seen_ids:
            seen_ids.add(thread_id)
            thread_name = f"Chat-{len(all_threads) + 1}"  # Name in order of appearance
            all_threads.append({'id': thread_id, 'name': thread_name})

    return all_threads

def delete_thread_messages(thread_id: str):
    """Delete all checkpoints related to a specific thread_id"""
    # This deletes all saved states related to the thread
    checkpointer.delete({'configurable': {'thread_id': thread_id}})



  
