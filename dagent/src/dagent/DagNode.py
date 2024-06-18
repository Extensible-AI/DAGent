
class DagNode:
    def __init__(
        self, 
        func: callable, 
        next_nodes: dict[str, 'DagNode'] = None
    ):
        self.func = func
        self.next_nodes = next_nodes or {}
        self.node_result = None

    def compile(self):
        """
        Use an LLM to generate tool descriptions from functions to run the DAG
        """
        return NotImplemented

    def run(self, **kwargs) -> any:
        raise NotImplementedError("Subclasses should implement this method")