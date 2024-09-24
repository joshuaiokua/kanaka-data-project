"""
LLM Tools

Functions for working with tools in the LangChain and LangGraph.

NOTE: Tools, as defined by a `@tool` decorator or as an extension of the BaseTool class, are functions that can be used within a LangChain or LangGraph model to perform specific tasks. This requires these functions' documentation to be formatted with an LLM model, rather than a human user, in mind. This also requires that some functionality be rewritten. For example, you may need to suppress actual error messages and return a generic error message instead as seen in `db_query_tool`.

Functions:
    get_tool: Get a tool from a list of tools by name.
    get_tool_calls: Get the tool calls from the graph's given State.
    handle_tool_error: Handle errors that occur during the execution of a tool.
    create_tool_node: Create a ToolNode with or without fallbacks.
    create_tool_call: Call the tool(s) specified by the function's tool arguments.
    create_tooled_agent: Create an agent (i.e. LLM model) with tools bound to it.
"""

# External Libraries
from typing import Callable, Type

from langchain_core.messages import AIMessage, AnyMessage, ToolMessage
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field, create_model
from langchain_core.runnables import (
    Runnable,
    RunnableBinding,
    RunnableLambda,
    RunnableWithFallbacks,
)
from langchain_core.tools import Tool
from langgraph.prebuilt import ToolNode

# Internal Libraries
from src.utilities.common import create_random_identifier, get_attribute

from .utils import ChatModel, State, Toolkit

### --- MODULE CONSTANTS --- ###
QUERY_ERROR_MESSAGE = (
    "Error: Query is not correct. Please rewrite the query and try again."
)
WRONG_TOOL_MESSAGE = "Error: The wrong tool was called {tool_name}. Please fix your mistakes. Remember to only call {required_tool} to submit the final answer. Generated queries should be outputted WITHOUT a tool call."


### --- FUNCTIONS --- ###
def get_tool_name(tool: Tool | Type[Tool]) -> str:
    """
    Get the name of a tool from a tool object or class.
    """
    return get_attribute(tool, "name")


def get_tool(tools: list[Tool] | Toolkit, tool_name: str) -> Tool:
    """
    Get a tool from a list of tools by name, such as those returned by a toolkit's `get_tools` method.
    """
    # handle if tools are a Toolkit object
    if not isinstance(tools, list):
        tools = tools.get_tools()

    for tool in tools:
        if get_tool_name(tool) == tool_name:
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


def catch_hallucinations(
    message: AnyMessage,
    required_tool: str | Type[Tool],
    tool_message: str = WRONG_TOOL_MESSAGE,
) -> list | list[ToolMessage]:
    """
    Catch potential hallucinations and generate a query to verify the user's intent.

    Args:
        message (AnyMessage): The message to check for hallucinations.
        required_tool (str | Type[Tool]): The tool that should be used to submit the final answer.
        tool_message (str, optional): The message to display when the wrong tool is called. Defaults to WRONG_TOOL_MESSAGE.
    """
    # Cast required_tool to string if it is a Tool object
    if not isinstance(required_tool, str):
        required_tool = get_tool_name(required_tool)

    tool_messages = [
        ToolMessage(
            content=tool_message.format(
                tool_name=tool_call["name"],
                required_tool=required_tool,
            ),
            tool_call_id=tool_call["id"],
        )
        for tool_call in message.tool_calls
        if tool_call["name"] != required_tool
    ]

    return {"messages": [message, *tool_messages]}


def create_simple_tool_class(
    tool_name: str,
    description: str,
    fields: dict[str, tuple[type, str]],
) -> Type[BaseModel]:
    """
    Dynamically create a simple tool class with explanatory docstrings and fields for use by the LLM agent.

    NOTE: This function is meant for simple tools that do not return complex data structures. To create more complex tools, consider using LangChain's `BaseTool` class.

    Args:
        tool_name (str): The name of the tool class.
        description (str): The docstring explaining the tool's purpose to the agent.
        fields (dict[str, tuple[type, str]]): A dictionary where keys are field names and values are tuples of (field type, field description).

    Returns:
        Type[BaseModel]: A dynamically generated Pydantic model class.
    """
    # Process the fields to include descriptions with Field
    field_definitions = {
        field_name: (field_type, Field(..., description=field_desc))
        for field_name, (field_type, field_desc) in fields.items()
    }

    # Create the Pydantic model dynamically
    tool_class = create_model(tool_name, **field_definitions)

    # Set the docstring
    tool_class.__doc__ = description

    return tool_class


def create_tool_node(
    tool: Tool | list[Tool],
    with_fallbacks: bool = True,
    fallbacks: list[Callable] | None = None,
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


def create_tool_call(
    tool_name: str,
    tool_args: dict | None = None,
    tool_id: str | None = None,
    message_content: str = "",
) -> dict:
    """
    Call the tool(s) specified by the function's tool arguments.
    """
    return {
        "messages": [
            AIMessage(
                content=message_content,
                tool_calls=[
                    {
                        "name": tool_name,
                        "args": tool_args if tool_args else {},
                        "id": tool_id if tool_id else create_random_identifier("tool"),
                    },
                ],
            ),
        ],
    }


def create_tooled_agent(
    model: ChatModel,
    tools: list[Tool] | str,
    tool_choice: str | dict = "auto",
    prompt_template: PromptTemplate | None = None,
    agent_description: str | None = None,
    inherit_tool_description: bool = True,
    model_kwargs: dict | None = None,
) -> RunnableBinding:
    """
    Create an agent (i.e. LLM model) with tools bound to it.

    Args:
        model (ChatModel): The model to bind tools to.
        tools (list[Tool] | str): The tool(s) to bind to the model.
        tool_choice (str | dict, optional): The tool or tool choice strategy to bind to the model. Defaults to "auto".
        prompt_template (PromptTemplate, optional): The prompt template to feed to the model. Defaults to None.
        agent_description (str, optional): The description of the agent for contextual use by the LLM graph. Defaults to tool description.
        inherit_tool_description (bool, optional): Whether to inherit the tool's description for the agent. Defaults to True.
        model_kwargs (dict, optional): Keyword arguments to pass to the model, such as:
            - model
            - temperature
    """
    # Initialize model with keyword arguments if provided
    if model_kwargs is not None:
        model = model(**model_kwargs)

    # Cast tools to list if not already
    tools = [tools] if not isinstance(tools, list) else tools

    # Handle `required` tool choice
    if tool_choice == "required":
        if len(tools) != 1:
            raise ValueError("Exactly one tool is needed for 'required' tool choice.")
        tool_choice = tools[0].name  # sets to the name of the only tool

    # Add prompt template if provided
    if prompt_template is not None:
        agent = prompt_template | model.bind_tools(tools=tools, tool_choice=tool_choice)
    else:
        agent = model.bind_tools(tools=tools, tool_choice=tool_choice)

    # Set the agent description if provided
    if agent_description is not None:
        agent.__doc__ = agent_description
    if inherit_tool_description and hasattr(tools[0], "description"):
        agent.__doc__ = tools[0].description
    elif inherit_tool_description and hasattr(tools[0], "__doc__"):
        agent.__doc__ = tools[0].__doc__

    return agent


### --- TOOLS --- ###
