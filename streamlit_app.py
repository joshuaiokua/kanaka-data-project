"""
Streamlit Application

Entrypoint file for Streamlit application.
"""
# ruff: noqa: B018

import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import MemorySaver

from src.frontend import load_model
from src.llmcore import create_simple_chatbot

load_dotenv()

### --- CONFIGURATION --- ###
model = ChatGroq(model="llama-3.1-70b-versatile")
memory = MemorySaver()

# Load the model
app = load_model(
    model,
    create_simple_chatbot,
    memory=memory,
)

config = {"configurable": {"thread_id": 1}}

### --- STREAMLIT APP --- ###

context = (
    "***Mo'olelo***: the narrative stories of the Kanaka Maoli (i.e. Native Hawaiians)."
)
st.title("Data Mo'olelo", help=context)


def generate_response(input_text):
    output = app.invoke({"messages": HumanMessage(content=input_text)}, config)
    return output["messages"][-1].content


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Aloha, howzit?"},
    ]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = generate_response(prompt)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
