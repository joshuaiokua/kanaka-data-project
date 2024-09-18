"""
Utility functions and helpful type aliases for interacting with LLM architecture, primarily as defined by LangChain and LangGraph.
"""
import re

from langchain_core.language_models import BaseChatModel, SimpleChatModel
from langchain_core.pydantic_v1 import BaseModel
from langgraph.graph import StateGraph
from typing_extensions import TypedDict

### --- CONSTANTS --- ###
MODEL_PROVIDERS = {"openai", "groq"}

### --- TYPE ALIASES --- ###
type State = TypedDict | BaseModel
type ChatModel = BaseChatModel | SimpleChatModel


### --- FUNCTIONS --- ###
def show_graph(graph: StateGraph) -> None:
    """Show the graph."""
    from IPython.display import Image, display

    return display(
        Image(
            graph.get_graph().draw_mermaid_png(),
        ),
    )


def get_model_provider(model: object) -> str:
    """
    Get the provider (e.g. Groq, OpenAI, etc.) of a model object.
    """
    match = re.search(
        r"langchain_([a-zA-Z0-9_]+)",
        model.__module__,
    )
    if match:
        return match.group(1)
    raise ValueError("Model provider not found.")


def list_models(provider: str = "groq", sparse: bool = True) -> list:
    """
    List the available models from a given provider.

    Args:
        provider (str): The LLM provider (e.g. OpenAI, Groq, etc.). Defaults to "groq".
        sparse (bool): Whether to return only the model IDs (i.e names). Defaults to True.
    """
    match provider.lower():
        case "openai":
            from openai import OpenAI

            client = OpenAI()
        case "groq":
            from groq import Groq

            client = Groq()
        case _:
            msg = (
                f"Provider {provider} not recognized. Must be one of {MODEL_PROVIDERS}."
            )
            raise ValueError(msg)

    models = client.models.list().data
    if sparse:
        return [model.id for model in models]
    return models


def handle_model_selection(provider: object, model: str | None = None) -> str:
    """
    Handle model selection.
    """

    def _handle_model_mismatch(model_provider: str, model: str) -> str:
        provider_model_mismatch_msg = (
            f"`{model_provider}` does not support model `{model}`."
        )
        models = list_models(model_provider)
        if model and model in models:
            return model
        raise ValueError(provider_model_mismatch_msg)

    model_provider = get_model_provider(provider)
    match model_provider:
        case "openai":
            if model:
                return _handle_model_mismatch("openai", model)
            return "gpt-4o"
        case "groq":
            if model:
                return _handle_model_mismatch("groq", model)
            return "llama3-groq-70b-8192-tool-use-preview"
        case _:
            msg = f"Unknown model provider: {provider}"
            raise ValueError(msg)
