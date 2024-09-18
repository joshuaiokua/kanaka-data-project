"""
Functions for working with graphs in the LangChain and LangGraph.
"""

# External Libraries
from itertools import pairwise
from typing import Annotated, Literal

from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import AnyMessage, add_messages
from langgraph.graph.state import CompiledStateGraph
from typing_extensions import TypedDict

# Internal Libraries
from .utils import State, show_graph


### --- CLASSES --- ###
class SimpleState(TypedDict):
    """Simplest allowable graph state for a LangGraph workflow construction."""

    messages: Annotated[list[AnyMessage], add_messages]


class SimpleGraphBuilder:
    """
    Simple StateGraph builder, usable for graphs with sequential nodes and connections and most appropriate for quick prototyping.
    """

    def __init__(
        self,
        state: State,
        nodes: list[tuple[str, callable]],
    ) -> None:
        """
        Initialize the SimpleGraphBuilder with the given state and nodes.
        """

        # Initialize graph
        self.state = state
        self.graph = StateGraph(state)

        # Add nodes
        for node in nodes:
            self.graph.add_node(*node)

        # Connect nodes
        for origin, target in pairwise([START, *self.graph.nodes.keys(), END]):
            self.graph.add_edge(origin, target)

        # Remaining parameters
        self.app = None

    def compile(self) -> CompiledStateGraph:
        """
        Compile the graph, calling to the graph object's compile method.
        """
        self.app = self.graph.compile()
        return self.app

    def show(self) -> None:
        """
        Display the graph.
        """
        if not self.app:
            raise ValueError("Graph hasn't yet been compiled.")
        show_graph(self.app)
