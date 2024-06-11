from typing import Callable, Any, Dict
from .DAG_Node import DAG_Node

class DAG_Node:
    def __init__(
        self, 
        func: Callable, 
        next_nodes: Dict[str, DAG_Node] = None
    ):
        self.func = func
        self.next_nodes = next_nodes or {}
        self.node_result = None

    def compile(self):
        """
        Use an LLM to generate tool descriptions from functions to run the DAG
        """
        return NotImplemented

    def run(self, *args, **kwargs) -> Any:
        raise NotImplementedError("Subclasses should implement this method")