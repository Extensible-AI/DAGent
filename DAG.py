from typing import Callable, Any, Dict

class Node:
    def __init__(self, func: Callable, next_nodes: Dict[str, 'Node'] = None):
        self.func = func
        # next_nodes is a dictionary mapping output values to the next Node
        self.next_nodes = next_nodes or {}
        self.node_result = None

    def run(self, *args, **kwargs) -> Any:
        self.node_result = self.func(*args, **kwargs)
        # Determine the next node based on the function's output
        if self.next_nodes and isinstance(self.node_result, str) and self.node_result in self.next_nodes:
            return self.next_nodes[self.node_result].run(*args, **kwargs)
        return self.node_result

class DAGent:
    def __init__(self, entry_node: Node):
        self.entry_node = entry_node

    def execute(self, *args, **kwargs):
        return self.entry_node.run(*args, **kwargs)

def tool_use_llm_task(input_text: str) -> str:
    # This function simulates an LLM decision.
    # Replace it with actual LLM interaction code.
    # For example, based on input_text, decide which node to execute next.
    if "special" in input_text:
        return "specialTask"
    else:
        return "defaultTask"

def main():
    # Define the workflow with dynamic next-node selection
    special_node = Node(func=lambda x: f"Special processing of {x}")
    default_node = Node(func=lambda x: f"Default processing of {x}")
    entry_node = Node(func=tool_use_llm_task, next_nodes={"specialTask": special_node, "defaultTask": default_node})

    dag = DAGent(entry_node=entry_node)

    # Execute the DAG
    result = dag.execute("hello world with special")
    print(result)

    res2 = dag.execute("hello world")
    print(res2)

if __name__ == "__main__":
    main()