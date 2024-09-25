"""
Streamlit Application

Entrypoint file for Streamlit application.
"""
# ruff: noqa: B018

import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import MemorySaver

from src.frontend.streamlit import (
    generate_response,
    initialize_chat,
    load_model,
    show_chat_messages,
)
from src.llmcore import create_simple_chatbot

load_dotenv()

### --- CONFIGURATION --- ###
SESSION = st.session_state

app = load_model(
    _model=ChatGroq(model="llama-3.1-70b-versatile"),
    _graph_builder=create_simple_chatbot,
    _memory=MemorySaver(),
)
config = {"configurable": {"thread_id": 1}}

### --- STREAMLIT APP --- ###
context = (
    "***Mo'olelo***: the narrative stories of the Kanaka Maoli (i.e. Native Hawaiians)."
)
st.title("Data Mo'olelo", help=context)

# Initialize chat history
initialize_chat(SESSION, starting_message="Aloha, howzit?")

# Display chat messages from history on app rerun
show_chat_messages(SESSION)

# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    SESSION.messages.append({"role": "user", "content": prompt})

    response = generate_response(prompt, app, config)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    SESSION.messages.append({"role": "assistant", "content": response})
