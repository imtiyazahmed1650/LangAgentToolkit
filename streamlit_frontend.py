import streamlit as st
from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage

thread_id ='1'
CONFIG = {'configurable': {'thread_id':thread_id}}
if 'message_history' not in st.session_state:
    st.session_state ['message_history'] = []

message_history = []

# loading the conversation history
for message in st.session_state ['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

user_input = st.chat_input('Type Hhere')

if user_input:
    
    # first append the list to message history
    st.session_state ['message_history'].append({'role':'user','content':user_input})
    with st.chat_message('user'):
        st.text(user_input)

    response = chatbot.invoke({'messages': [HumanMessage(content=user_input)]},config=CONFIG)
    ai_message = response['messages'][-1].content
    # first append the list to message history
    st.session_state ['message_history'].append({'role':'assitant','content':ai_message})
    with st.chat_message('assistant'):
        st.text(ai_message)