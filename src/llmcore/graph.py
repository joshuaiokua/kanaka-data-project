"""
LLM Graphs

Functions and Classes for working with and in StateGraph objects in LangGraph.

Classes:
    SimpleState: Simplest allowable graph state for a LangGraph workflow construction.
    SimpleGraphBuilder: Graph builder usable for simple graphs with sequential nodes and connections.

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
        complete_build: bool = True,
    ) -> None:
        """
        Initialize the SimpleGraphBuilder with the given state and nodes.

        Args:
            state (State): The base state to use for the graph.
            nodes (list[tuple[str, callable]]): The nodes to add to the graph, each as a tuple of the node's name and the node's defining functionality.
            complete_build (bool): Whether to add END to the graph, allowing it to be compiled as a complete graph after right after initialization. Defaults to True.
        """

        # Initialize graph
        self.state = state
        self.graph = StateGraph(state)

        # Add nodes
        for node in nodes:
            self.graph.add_node(*node)

        # Connect nodes
        _nodes = [START, *self.graph.nodes.keys()]
        if complete_build:
            _nodes.append(END)

        for origin, target in pairwise(_nodes):
            self.graph.add_edge(origin, target)

        # Remaining parameters
        self.app = None

    def add_node(self, name: str, functionality: callable, **kwargs) -> None:
        """
        Add a node to the graph.

        Args:
            name (str): The name of the node.
            functionality (callable): The functionality of the node.
            kwargs: Additional keyword arguments to pass to the graph's add_node method.
        """
        self.graph.add_node(name, functionality, **kwargs)

    def add_edge(self, origin: str, target: str, **kwargs) -> None:
        """
        Add an edge to the graph.

        Args:
            origin (str): The origin node.
            target (str): The target node.
            kwargs: Additional keyword arguments to pass to the graph's add_edge method.
        """
        self.graph.add_edge(origin, target, **kwargs)

    def add_conditional_edges(
        self,
        origin: str,
        target: callable,
        **kwargs,
    ) -> None:
        """
        Add conditional edges to the graph.

        Args:
            origin (str): The origin node.
            target (str | callable): The target node or a callable that returns the target node.
            kwargs: Additional keyword arguments to pass to the graph's add_conditional_edges method.
        """
        self.graph.add_conditional_edges(origin, target, **kwargs)

    def compile(self, **kwargs) -> CompiledStateGraph:
        """
        Compile the graph, calling to the graph object's compile method.
        """
        self.app = self.graph.compile(**kwargs)
        return self.app

    def show(self) -> None:
        """
        Display the graph.
        """
        if not self.app:
            raise ValueError("Graph hasn't yet been compiled.")
        show_graph(self.app)
