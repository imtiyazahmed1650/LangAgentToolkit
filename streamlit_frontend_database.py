import streamlit as st
from langgraph_database_backend import chatbot, retrieve_all_threads, delete_thread_messages
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

def delete_chat_and_update_state(thread_id_to_delete, thread_name_to_delete):
    # This is the critical step: deleting the chat from the permanent database storage.
    #delete_thread_messages(str(thread_id_to_delete))

    st.sidebar.info(f"Preparing to delete chat: {thread['name']} (ID: {thread['id']})")
    #st.toast(f"Deleting chat: {thread['name']}", icon='🗑️')
    

# **************************************** Session Setup ******************************
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = retrieve_all_threads()

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
    # Use columns to place the delete button next to the conversation name
    col1, col2 = st.sidebar.columns([0.8, 0.2])
    
    with col1:
        if st.button(thread['name'], key=f"load_{thread['id']}"):
            st.session_state['thread_id'] = thread['id']
            messages = load_conversation(thread['id'])
            temp_message = []
            for msg in messages:
                role = 'user' if isinstance(msg, HumanMessage) else 'assistant'
                temp_message.append({'role': role, 'content': msg.content})
            st.session_state['message_history'] = temp_message

    with col2:
        # The delete button with a trash can emoji
        if st.button('🗑️', key=f"delete_{thread['id']}"):
            # Call the function to delete the chat
            delete_chat_and_update_state(thread['id'], thread['name'])

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