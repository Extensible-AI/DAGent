from .DAG_Node import DAG_Node
from typing import Callable, Any, Dict, Optional

class FunctionNode(DAG_Node):
    def __init__(self, func: Callable, next_nodes: Dict[str, DAG_Node] = None):
        super().__init__(func, next_nodes)

    def run(self, *args, **kwargs) -> Any:
        # Run the function and store the result
        self.node_result = self.func(*args, **kwargs)
        # Pass the result to the next nodes if any
        for _, next_node in self.next_nodes.items():
            next_node.run(self.node_result, **(kwargs or {}))

