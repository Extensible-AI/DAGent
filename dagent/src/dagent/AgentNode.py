import json
import inspect
from .DagNode import DagNode
from .base_functions import call_llm_tool


class AgentNode(DagNode):
    def __init__(
        self, 
        func: callable, 
        next_nodes: dict[str, DagNode] = None,
        user_params: dict | None = None  
    ):
        super().__init__(func, next_nodes)
        self.user_params = user_params or {}

    def run(self, **kwargs) -> any:
        if not self.next_nodes:
            raise ValueError("Next nodes not specified for LLM call")

        try:
            response = call_llm_tool(tools=[node.tool_description for node in self.next_nodes.values()], **kwargs)
            tool_calls = getattr(response, 'tool_calls', None)
            if not tool_calls:
                raise ValueError("No tool calls received from LLM tool response")

            # TODO: Should there be a pattern for restricting calls - error if multiple?
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                next_node = self.next_nodes.get(function_name)
                if not next_node:
                    raise KeyError(f"Function name '{function_name}' not found in next_nodes")

                # Merge user_params with function_args, giving precedence to user_params
                merged_args = {**function_args, **self.user_params}
                func_signature = inspect.signature(next_node.func)
                # TODO: add pydantic validation + cover in compile method
                filtered_args = {k: v for k, v in merged_args.items() if k in func_signature.parameters}

                next_node.run(**filtered_args)

        except (AttributeError, json.JSONDecodeError) as e:
            raise ValueError(f"Error parsing tool call: {e}")
        except Exception as e:
            raise RuntimeError(f"LLM tool call failed: {e}")
