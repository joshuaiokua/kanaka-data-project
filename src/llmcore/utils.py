"""
Utility functions and helpful type aliases for interacting with LLM architecture, primarily as defined by LangChain and LangGraph.
"""

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


def list_models(provider: str = "groq") -> list:
    """List the available models from a given provider."""
    match provider.lower():
        case "openai":
            from openai import OpenAI

            client = OpenAI()
        case "groq":
            from groq import Groq

            client = Groq()
        case _:
            msg = f"Provider {provider} not recognized. Must be one of {MODEL_PROVIDERS}."
            raise ValueError(msg)

    return client.models.list().data
