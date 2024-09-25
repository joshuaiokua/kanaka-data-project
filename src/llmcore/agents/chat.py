"""
Chatbot Agents

Collection of classes and functions for conversational LLM agents (i.e. chatbots).
"""

# External Libraries
from langgraph.graph.state import CompiledStateGraph

# Local Libraries
from src.llmcore.graph import SimpleGraphBuilder, SimpleState
from src.llmcore.utils import ChatModel, Memory


### --- FUNCTIONS --- ###
def create_simple_chatbot(
    model: ChatModel,
    memory: Memory | None = None,
    **kwargs,
) -> CompiledStateGraph:
    """
    Create a simple chatbot agent.

    Args:
        model (ChatModel): The chatbot model to use.
        memory (Memory, optional): The memory object to use for the chatbot agent. Defaults to None.
        **kwargs: Additional keyword arguments to pass to the graph compiler.

    Returns:
        CompiledStateGraph: The compiled state graph for the chatbot agent.
    """
    graph = SimpleGraphBuilder(
        state=SimpleState,
        nodes=[
            (
                "chatbot",
                lambda state: {"messages": [model.invoke(state["messages"])]},
            ),
        ],
        complete_build=True,
    )

    return graph.compile(
        checkpointer=memory if memory else None,
        **kwargs,
    )
