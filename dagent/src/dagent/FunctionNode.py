from .DagNode import DagNode

class FunctionNode(DagNode):
    def __init__(self, func: callable, tool_description = dict | None, next_nodes: dict[str, DagNode] = None, user_params: dict | None = None):
        super().__init__(func, next_nodes)
        self.tool_description = tool_description
        self.user_params = user_params or {}
        self.compiled = False
    
    def compile(self) -> None:
        self.compiled = True
        if isinstance(self.next_nodes, list):
            self.next_nodes = {node.func.__name__: node for node in self.next_nodes}
        for _, next_node in self.next_nodes.items():
            next_node.compile()

    def run(self, **kwargs) -> any:
        if not self.compiled:
            raise ValueError("Node not compiled. Please run compile() method from the entry node first")

        self.node_result = self.func(**kwargs)
        # Pass the result to the next nodes if any
        # TODO: figure out param logic pattern
        if not self.next_nodes:
            return self.node_result
        for _, next_node in self.next_nodes.items():
            # TODO: creating data models for passing info between nodes 
            params = {'prev_output': self.node_result, **next_node.user_params}
            next_node.run(**params)
