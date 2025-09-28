from langgraph.graph import StateGraph,START,END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph.message import add_messages
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langgraph.checkpoint.memory import MemorySaver
from dotenv import load_dotenv
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
# llama3-8b-8192

def ChatNode(state : ChatState) -> dict:
    """Chatbot node: takes messages from state and generates reply"""
    response = model.invoke(state["messages"])
    return {"messages":  [response]}


checkpointer = MemorySaver()

graph = StateGraph(ChatState)
graph.add_node("chatbot", ChatNode)
graph.add_edge(START, "chatbot")
graph.add_edge("chatbot", END)
 

chatbot = graph.compile(checkpointer=checkpointer)

# Stream logic
# for message_chunk, metadata in chatbot.stream(
#     {'messages': [HumanMessage(content='What is the Recipe of Pasta')]},config={'configurable': {'thread_id':'thread_id_1'}},
#     stream_mode= 'messages'
# ):
#     if message_chunk.content:
#         print(message_chunk.content, end=" ", flush=True)

# thread_id = '1'
# while True:
#     user_message = input('Type here : ')
#     if user_message.strip().lower() in ['exit','quit','bye']:
#         break
    
#     config = {'configurable': {'thread_id':thread_id}}
#     response = workflow.invoke({'messages': [HumanMessage(content=user_message)]},config=config)
#     print('AI : ',response['messages'][-1].content)

