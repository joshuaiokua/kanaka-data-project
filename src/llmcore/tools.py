"""
Functions for working with tools in the LangChain and LangGraph.

NOTE: Tools, as defined by a `@tool` decorator or as an extension of the BaseTool class, are functions that can be used within a LangChain or LangGraph model to perform specific tasks. This requires these functions' documentation to be formatted with an LLM model, rather than a human user, in mind. This also requires that some functionality be rewritten. For example, you may need to suppress actual error messages and return a generic error message instead as seen in `db_query_tool`.
"""

# External Libraries
from typing import Type

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain.pydantic_v1 import BaseModel, Field
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_core.messages import ToolMessage
from langchain_core.runnables import (
    Runnable,
    RunnableBinding,
    RunnableLambda,
    RunnableWithFallbacks,
)
from langchain_core.tools import BaseTool, Tool
from langgraph.prebuilt import ToolNode

# Internal Libraries
from src.utils import get_class_name

from .utils import ChatModel, State

### --- CONSTANTS --- ###
QUERY_ERROR_MSG = "Error: Query is not correct. Please rewrite the query and try again."


### --- FUNCTIONS --- ###
def get_tool(tools: list[Tool], tool_name: str) -> Tool:
    """
    Get a tool from a list of tools by name, such as those returned by a toolkit's `get_tools` method.
    """
    for tool in tools:
        if tool.name == tool_name:
            return tool
    msg = f"Tool '{tool_name}' not found in list of tools."
    raise ValueError(msg)


def get_tool_calls(
    state: State,
    message_index: int = -1,
) -> list[dict]:
    """
    Get the tool calls from the graph's given State, defaulting to the last message unless otherwise specified by `message_index`.

    TODO: Generalize this function to work with non-State objects (e.g. AIMessage).
    """
    try:
        return state["messages"][message_index].tool_calls
    except AttributeError as e:
        raise AttributeError("Message does not have any tool calls.") from e


def handle_tool_error(state: State) -> dict:
    """
    Handle errors that occur during the execution of a tool.
    """
    error = state.get("error")
    tool_calls = get_tool_calls(state)

    return {
        "messages": [
            ToolMessage(
                content=f"Error: {error!r}\n please fix your mistakes.",
                tool_call_id=tc["id"],
            )
            for tc in tool_calls
        ],
    }


def create_tool_node(
    tool: Tool | list[Tool],
    with_fallbacks: bool = True,
    fallbacks: list[callable] | None = None,
) -> ToolNode | Runnable | RunnableWithFallbacks:
    """
    Create a ToolNode with or without fallbacks.

    Args:
        tool (Tool | list[Tool]): The tool or tools to use.
        with_fallbacks (bool): Whether to include fallbacks.
        fallbacks (list[callable]): The fallbacks to use. Defaults to None, in which case handle_tool_error is used.
    """
    # Cast tool(s) to list if not already
    tools = [tool] if not isinstance(tool, list) else tool

    # Set the fallbacks to handle_tool_error if not provided
    fallbacks = [handle_tool_error] if fallbacks is None else fallbacks

    if with_fallbacks:
        return ToolNode(tools).with_fallbacks(
            [RunnableLambda(fb) for fb in fallbacks],
            exception_key="error",
        )
    return ToolNode(tools)


def bind_tools(
    model: ChatModel,
    tools: list,
    tool_choice: str | dict = "auto",
) -> RunnableBinding:
    """
    Bind tools to a model, accounting for how Groq handles `tool_choice`. Functions as a wrapper for `model.bind_tools` method.
    """
    # Handle Groq models with `tool_choice = required`
    if "Groq" in get_class_name(model) and tool_choice == "required":
        if len(tools) > 1:
            raise ValueError(
                "Groq allows only one tool to be used when `tool_choice = required`.",
            )
        tool_choice = {"type": "function", "function": {"name": tools[0].name}}

    return model.bind_tools(tools, tool_choice=tool_choice)


def create_tooled_model(
    model: ChatModel,
    tools: list[Tool],
    tool_choice: str | dict,
    model_kwargs: dict | None = None,
) -> RunnableBinding:
    """
    Create a model with tools bound to it, accounting for how Groq handles `tool_choice`. Functions as a wrapper for `bind_tools` method.

    Args:
        model (ChatModel): The model to bind tools to.
        tools (list[Tool]): The tool(s) to bind to the model.
        tool_choice (str | dict): The tool choice to use (e.g. "required", "auto", etc.).
        model_kwargs (dict): Keyword arguments to pass to the model, such as:
            - model
            - temperature
    """
    if model_kwargs is not None:
        model = model(**model_kwargs)

    return bind_tools(model, tools, tool_choice)


### --- TOOLS --- ###
