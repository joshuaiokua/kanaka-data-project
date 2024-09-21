"""
Streamlit Application

Entrypoint file for Streamlit application.
"""
# ruff: noqa: B018

import numpy as np
import pandas as pd
import streamlit as st

context = "***Mo'olelo***: the narrative stories of the Kanaka Maoli (i.e. Native Hawaiians)."
st.title("Data Mo'olelo", help=context)

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

    response = ":call_me_hand: :call_me_hand: :call_me_hand:"
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
