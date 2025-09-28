import streamlit as st
from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage, AIMessage
import uuid


# **************************************** utility functions *************************
def generate_thread_id():
    return uuid.uuid4()


def reset_chat():
    new_thread_id = generate_thread_id()
    st.session_state['thread_id'] = new_thread_id
    
    # Generate a new chat name based on existing threads count
    new_chat_name = f"Chat-{len(st.session_state['chat_threads']) + 1}"
    
    add_thread({'id': new_thread_id, 'name': new_chat_name})
    st.session_state['message_history'] = []


def add_thread(thread):
    # thread is a dict {'id': UUID, 'name': str}
    if all(t['id'] != thread['id'] for t in st.session_state['chat_threads']):
        st.session_state['chat_threads'].append(thread)


def load_conversation(thread_id):
    state = chatbot.get_state(config={'configurable': {'thread_id': thread_id}})
    return state.values.get('messages', [])


# **************************************** Session Setup ******************************

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = []

# On first run, if no thread yet, add the initial thread with a name
if not st.session_state['chat_threads']:
    initial_thread_name = "Chat-1"
    add_thread({'id': st.session_state['thread_id'], 'name': initial_thread_name})


# **************************************** Sidebar UI *********************************

st.sidebar.title('LangGraph Chatbot')

if st.sidebar.button('New Chat'):
    reset_chat()

st.sidebar.header('My Conversations')

for thread in st.session_state['chat_threads'][::-1]:  # reverse to show latest on top
    if st.sidebar.button(thread['name']):
        st.session_state['thread_id'] = thread['id']
        messages = load_conversation(thread['id'])
        temp_message = []
        for msg in messages:
            if isinstance(msg, HumanMessage):
                role = 'user'
            else:
                role = 'assistant'
            temp_message.append({'role': role, 'content': msg.content})

        st.session_state['message_history'] = temp_message


# **************************************** Main UI ************************************

for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])


user_input = st.chat_input('Type here')

if user_input:

    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)

    CONFIG = {'configurable': {'thread_id': st.session_state['thread_id']}}

    with st.chat_message('assistant'):
        def ai_only_stream():
            for message_chunk, metadata in chatbot.stream(
                {'messages': [HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode='messages'
            ):
                if isinstance(message_chunk, AIMessage):
                    yield message_chunk.content
        
        ai_message = st.write_stream(ai_only_stream())

    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})
