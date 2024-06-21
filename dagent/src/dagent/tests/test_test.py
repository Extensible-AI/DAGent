from dagent import AgentNode, FunctionNode


def func1(a: int, b: int) -> int:
    return a + b

func1_node = FunctionNode(func1)
func2_node = FunctionNode(func1)

agent_node = AgentNode(
    next_nodes={'func1': func1_node},
    func=lambda **kwargs: print(f"example  {kwargs}"),
)

agent_node.compile()