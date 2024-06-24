from dagent import DecisionNode, FunctionNode


def add_two_nums(a: int, b: int) -> int:
    return a + b


def multiply_two_nums(a: int, b: int) -> int:
    return a * b


def print_result(prev_output:int) -> None:
    print(prev_output)

# Setup function nodes
add_two_nums_node = FunctionNode(func=add_two_nums)
multiply_two_nums_node = FunctionNode(func=multiply_two_nums)
print_result_node = FunctionNode(func=print_result)

# Setup decision node
entry_node = DecisionNode()

# Link nodes together
entry_node.next_nodes = {
    add_two_nums_node.func.__name__: add_two_nums_node,
    multiply_two_nums_node.func.__name__: multiply_two_nums_node,
}

add_two_nums_node.next_nodes = {
    print_result_node.func.__name__: print_result_node
}

multiply_two_nums_node.next_nodes = {
    print_result_node.func.__name__: print_result_node
}

# Compile the nodes
entry_node.compile()

# Run the nodes
messages = [{"role": "user", "content": "add the numbers 2 and 3"}]


entry_node.run(model='gpt-3.5-turbo-0125', messages=messages)






