import json
from typing import Callable, Any, Dict, Optional
from .DAG_Node import DAG_Node
from .base_functions import call_llm_tool


class AgentNode(DAG_Node):
    def __init__(
        self, 
        func: Callable, 
        tool_description: Optional[Dict] = None, 
        next_nodes: Dict[str, DAG_Node] = None
    ):
        super().__init__(func, next_nodes)
        self.tool_description = tool_description

    def run(self, *args, **kwargs) -> Any:
        if not self.next_nodes:
            raise ValueError("Next nodes not specified for LLM call")

        try:
            response = call_llm_tool(tools=[node.tool_description for node in self.next_nodes.values()], **kwargs)
            tool_calls = getattr(response, 'tool_calls', None)
            if not tool_calls:
                raise ValueError("No tool calls received from LLM tool response")

            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                next_node = self.next_nodes.get(function_name)
                if not next_node:
                    raise KeyError(f"Function name '{function_name}' not found in next_nodes")

                next_node.run(**function_args)

        except (AttributeError, json.JSONDecodeError) as e:
            raise ValueError(f"Error parsing tool call: {e}")
        except Exception as e:
            raise RuntimeError(f"LLM tool call failed: {e}")
