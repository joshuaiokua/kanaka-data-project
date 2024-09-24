"""
Database Agents

Collection of classes and functions for LLM agents that interact with databases (e.g. SQL Agents, etc.).
"""

# External Libraries
from typing import Literal

from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.state import END, CompiledStateGraph

# Local Libraries
from src.datacore import load_local_database
from src.llmcore.graph import SimpleGraphBuilder, SimpleState
from src.llmcore.prompts import QUERY_GENERATION_SYSTEM_PROMPT, SimpleChatPromptTemplate
from src.llmcore.tools import (
    catch_hallucinations,
    create_simple_tool_class,
    create_tool_call,
    create_tool_node,
    create_tooled_agent,
    get_tool,
)
from src.llmcore.utils import ChatModel, State, handle_model_selection


def create_sql_agent(
    database: object,
    model_provider: object,
    model_config: dict | None = None,
) -> CompiledStateGraph:
    """
    Create a basic SQL agent, following LangGraph's "SQL Agent Tutorial" implementation.
    """
    ### --- CONFIGURATION --- ###

    # Configure Model
    model_config = model_config or {
        "model": handle_model_selection(model_provider),
        "temperature": 0,
    }

    # Get tools for interacting with the database
    toolkit = SQLDatabaseToolkit(
        db=database,
        llm=model_provider(model=model_config["model"]),
    )
    list_tables_tool = get_tool(toolkit, "sql_db_list_tables")
    get_schema_tool = get_tool(toolkit, "sql_db_schema")
    db_query_tool = get_tool(toolkit, "sql_db_query")
    query_check_tool = get_tool(toolkit, "sql_db_query_checker")

    ### --- BASE GRAPH CONSTRUCTION --- ###
    # Create Tool and Agent Nodes
    get_schema_agent = create_tooled_agent(
        model=model_provider,
        tools=get_schema_tool,
        model_kwargs=model_config,
    )

    # Create base graph
    graph = SimpleGraphBuilder(
        state=SimpleState,
        nodes=[
            (
                "first_tool_call",
                lambda state: create_tool_call("sql_db_list_tables"),  # noqa: ARG005
            ),
            (
                "list_tables_tool",
                create_tool_node(list_tables_tool),
            ),
            (
                "model_get_schema",
                lambda state: {
                    "messages": [get_schema_agent.invoke(state["messages"])],
                },
            ),
            (
                "get_schema_tool",
                create_tool_node(get_schema_tool),
            ),
        ],
        complete_build=False,
    )

    ### --- COMPLETE GRAPH CONSTRUCTION --- ###
    # Create Tool and Agent Nodes for more Complex Logic
    SubmitFinalAnswer = create_simple_tool_class(  # noqa: N806
        "SubmitFinalAnswer",
        "Submit the final answer to the user based on the query results.",
        {"final_answer": (str, "The final answer to the user")},
    )
    query_check_agent = create_tooled_agent(
        model=model_provider,
        tools=query_check_tool,
        tool_choice="required",
        model_kwargs=model_config,
    )
    query_gen_agent = create_tooled_agent(
        model=model_provider,
        tools=SubmitFinalAnswer,
        prompt_template=SimpleChatPromptTemplate(
            system_prompt=QUERY_GENERATION_SYSTEM_PROMPT,
        ),
        model_kwargs=model_config,
    )

    def query_gen_node(state: State) -> dict | None:
        """
        Generate a query based on the input question and schema.
        """
        message = query_gen_agent.invoke(state)
        return catch_hallucinations(message, SubmitFinalAnswer)

    def should_continue(
        state: State,
    ) -> Literal[END, "correct_query", "query_gen_node"]:
        """
        Decide whether to continue the workflow or end it.
        """
        messages = state["messages"]
        last_message = messages[-1]

        # If tool call then we finish
        if getattr(last_message, "tool_calls", None):
            return END
        if last_message.content.startswith("Error:"):
            return "query_gen_node"
        return "correct_query"

    # Add Nodes to the Graph
    graph.add_node("query_gen_node", query_gen_node)
    graph.add_node(
        "correct_query",
        lambda state: {
            "messages": [query_check_agent.invoke([state["messages"][-1]])],
        },
    )
    graph.add_node("execute_query", create_tool_node(db_query_tool))

    # Add Edges to the Graph
    graph.add_edge("get_schema_tool", "query_gen_node")
    graph.add_conditional_edges("query_gen_node", should_continue)
    graph.add_edge("correct_query", "execute_query")
    graph.add_edge("execute_query", "query_gen_node")

    # Compile and return the graph
    return graph.compile()
