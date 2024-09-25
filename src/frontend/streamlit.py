"""
Frontend Streamlit Module

Functions and classes for working with Streamlit for the project's frontend.

General Functions:
    initialize_chat: Initialize the Streamlit's chat history.
    show_chat_messages: Show the chat messages from the Streamlit session state, updating on rerun.
    generate_response: Generate a response from the chatbot agent.

Resource Functions:
    load_model: Load and cache a provided model and build a LangGraph for the Streamlit application.
"""

# External Libraries
from typing import Callable

import streamlit as st
from langchain_core.messages import HumanMessage
from streamlit.runtime.state import SessionState, SessionStateProxy

# Local Libraries
from src.llmcore.graph import CompiledStateGraph
from src.llmcore.utils import ChatModel, Memory


### --- RESOURCE FUNCTIONS --- ###
@st.cache_resource
def load_model(
    _model: ChatModel,
    _graph_builder: Callable,
    _memory: Memory | None = None,
    **kwargs,
) -> CompiledStateGraph:
    """
    Load and cache a provided model and build a L graph for the Streamlit application.

    Args:
        _model (ChatModel): The ChatModel to use for the model.
        _graph_builder (Callable): The graph builder to use for the model.
        _memory (Memory, optional): The memory object to use for the chatbot agent. Defaults to None.
        **kwargs: Additional keyword arguments to pass to the graph builder.
    """
    return _graph_builder(_model, _memory, **kwargs)


### --- GENERAL FUNCTIONS --- ###
def initialize_chat(
    session_state: SessionState | SessionStateProxy,
    starting_message: str,
    role: str = "assistant",
) -> None:
    """
    Initialize the Streamlit's chat history.

    Args:
        session_state (SessionState | SessionStateProxy): The Streamlit session state.
        starting_message (str): The starting message for the chat history.
        role (str, optional): The role of the starting message. Defaults to "assistant".
    """
    if "messages" not in session_state:
        session_state.messages = [
            {"role": role, "content": starting_message},
        ]


def show_chat_messages(session_state: SessionState | SessionStateProxy) -> None:
    """
    Show the chat messages from the Streamlit session state, updating the chat history on app rerun.
    """
    for message in session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def generate_response(
    input_text: str,
    agent: CompiledStateGraph,
    config: dict,
) -> str:
    """
    Generate a response from the chatbot agent.

    Args:
        input_text (str): The user input text.
        agent (CompiledStateGraph): The compiled state graph for the chatbot agent.
        config (dict): The thread configuration for the agent.

    Returns:
        str: The response from the chatbot agent.
    """
    output = agent.invoke(
        {"messages": HumanMessage(content=input_text)},
        config,
    )
    return output["messages"][-1].content
