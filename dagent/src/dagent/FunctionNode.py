from .DagNode import DagNode

class FunctionNode(DagNode):
    def __init__(self, func: callable, tool_description = dict | None, next_nodes: dict[str, DagNode] = None, user_params: dict | None = None):
        super().__init__(func, next_nodes)
        self.tool_description = tool_description
        self.user_params = user_params or {}

    def run(self, **kwargs) -> any:
        self.node_result = self.func(**kwargs)
        # Pass the result to the next nodes if any
        # TODO: figure out param logic pattern
        for _, next_node in self.next_nodes.items():
            # TODO: add pydantic validation + cover in compile method
            # 
            params = {'prev_output': self.node_result, **next_node.user_params}
            next_node.run(**params)
            # next_node.run(**)
