from .DAG_Node import DAG_Node

class FunctionNode(DAG_Node):
    def __init__(self, func: callable, tool_description = dict | None, next_nodes: dict[str, DAG_Node] = None, user_params: dict | None = None):
        super().__init__(func, next_nodes)
        self.tool_description = tool_description
        self.user_params = user_params or {}

    def run(self, **kwargs) -> any:
        self.node_result = self.func(**kwargs)
        # Pass the result to the next nodes if any
        for _, next_node in self.next_nodes.items():
            # next_node.run(self.node_result, **(kwargs or {}))
            next_node.run()
