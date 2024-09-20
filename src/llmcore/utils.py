"""
LLM Utilities

Utility functions and helpful type aliases for interacting with LLM architecture, primarily as defined by LangChain and LangGraph.

Types:
    State: A typed dictionary or Pydantic BaseModel representing the state of a StateGraph.
    ChatModel: A typed dictionary or Pydantic BaseModel representing an LLM chat model.

Functions:
    show_graph: Show the graph.
    get_model_provider: Get the provider (e.g. Groq, OpenAI, etc.) of a model object.
    list_models: List the available models from a given provider.
    handle_model_selection: Handle model selection.
    _handle_messages_object: Handle the messages object.
    get_last_message: Get the last message from the list of messages.
    print_messages: Print the messages.
    extract_sql_query: Extract the SQL query from the text.
"""

import re

from langchain_core.language_models import BaseChatModel, SimpleChatModel
from langchain_core.messages import AnyMessage
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


def get_model_provider(model: ChatModel) -> str:
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


def _handle_messages_object(
    messages: list[AnyMessage] | dict,
    messages_key: str = "messages",
) -> list[AnyMessage]:
    """
    Handle the messages object, returning the messages list if
    """
    if isinstance(messages, dict):
        return messages[messages_key]
    return messages


def get_last_message(
    messages: list[AnyMessage] | dict,
    **kwargs,
) -> str:
    """
    Get the last message from the list of messages.
    """
    messages = _handle_messages_object(messages, **kwargs)
    return messages[-1]


def print_messages(
    messages: list[AnyMessage] | dict,
    pretty_print: bool = True,
    **kwargs,
) -> None:
    """
    Print the messages.
    """
    messages = _handle_messages_object(messages, **kwargs)
    for message in messages:
        if pretty_print:
            message.pretty_print()
        else:
            print(message)


def extract_sql_query(text: str) -> str | None:
    """
    Extract the SQL query from the text (i.e. a message returned by a ChatModel).
    """
    match = re.search(
        pattern=r"```sql(.*?)```",
        string=text,
        flags=re.DOTALL,
    )

    if match:
        return match.group(1).strip()
    return None
