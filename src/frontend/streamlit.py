"""
Frontend Streamlit Module

Functions and classes for working with Streamlit in the project's frontend.
"""

# External Libraries
from typing import Callable

import streamlit as st

# Local Libraries
from src.llmcore.graph import CompiledStateGraph
from src.llmcore.utils import ChatModel


### --- FUNCTIONS --- ###
@st.cache_resource
def load_model(
    model: ChatModel,
    graph_builder: Callable,
    **kwargs,
) -> CompiledStateGraph:
    """
    Load and cache a provided model and build a L graph for the Streamlit application.

    Args:
        model (ChatModel): The ChatModel to use for the model.
        graph_builder (Callable): The graph builder to use for the model.
        **kwargs: Additional keyword arguments to pass to the graph builder.
    """
    return graph_builder(model, **kwargs)
