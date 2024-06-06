import json
from typing import Callable, Any, Dict, Optional
from base_functions import call_llm_tool
from icecream import ic

class Node:
    def __init__(self, func: Callable, is_llm_call: bool = False, tool_description: Optional[Dict] = None, next_nodes: Dict[str, 'Node'] = None):
        self.func = func
        # next_nodes is a dictionary mapping output values to the next Node
        self.next_nodes = next_nodes or {}
        self.is_llm_call = is_llm_call
        self.tool_description = tool_description
        self.node_result = None


    def run(self, *args, **kwargs) -> Any:
        if self.is_llm_call:
            # Call the LLM tool with the specified tool description
            if not self.next_nodes:
                raise ValueError("Next nodes not specified for LLM call")

            tool_descs = [node.tool_description for node in self.next_nodes.values()]
            # ic(tool_descs)
            
            try:
                response = call_llm_tool(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "randomly pick only one of the provided tools"}], tools=tool_descs)
            except Exception as e:
                raise RuntimeError(f"Failed to call LLM tool: {e}")

            if not hasattr(response, 'tool_calls'):
                raise AttributeError("Response from LLM tool does not have 'tool_calls' attribute")

            tool_calls = response.tool_calls
            ic(tool_calls)
            if not tool_calls:
                raise ValueError("No tool calls received from LLM tool response")

            for tool_call in tool_calls:
                try:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                except (AttributeError, json.JSONDecodeError) as e:
                    raise ValueError(f"Error parsing tool call: {e}")

                ic(function_name, function_args)
                if function_name not in self.next_nodes:
                    raise KeyError(f"Function name '{function_name}' not found in next_nodes")

                print('running function', function_name)
                # Dynamically unpack the function arguments into kwargs and pass them to the next node's run method
                try:
                    self.next_nodes[function_name].run(**function_args)
                except Exception as e:
                    raise RuntimeError(f"Failed to run function '{function_name}': {e}")
        else:
            # Run the function and store the result
            self.node_result = self.func(*args, **kwargs)
            if len(self.next_nodes) == 0:
                return self.node_result
            elif len(self.next_nodes) == 1:
                # assuming it is dependent on the result of this node
                self.next_nodes[0].run(self.node_result)
            else:
                for _, node in self.next_nodes.items():
                    # just runs whatever is next
                    node.run()

class DAGent:
    def __init__(self, entry_node: Node):
        self.entry_node = entry_node

    def execute(self, *args, **kwargs):
        return self.entry_node.run(*args, **kwargs)

def main():
    # Define the workflow with dynamic next-node selection
    get_calendar_events_node = Node(func=lambda **kwargs: print(f"get calendar events {kwargs}"), tool_description= {
            "type": "function",
            "function": {
                "name": "get_calendar_events",
                "description": "Get calendar events within a specified time range",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "start_time": {
                            "type": "string",
                            "description": "The start time for the event search, in ISO format",
                        },
                        "end_time": {
                            "type": "string",
                            "description": "The end time for the event search, in ISO format",
                        },
                    },
                    "required": ["start_time", "end_time"],
                },
            },
        })
    create_calendar_event_node = Node(func=lambda **kwargs: print(f"create calendar events {kwargs}"), tool_description={
            "type": "function",
            "function": {
                "name": "create_calendar_event",
                "description": "Create a calendar event with specified details",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "summary": {
                            "type": "string",
                            "description": "The summary or title of the event",
                        },
                        "start_time": {
                            "type": "string",
                            "description": "The start time of the event, in ISO format",
                        },
                        "end_time": {
                            "type": "string",
                            "description": "The end time of the event, in ISO format",
                        },
                        "description": {
                            "type": "string",
                            "description": "The description of the event (optional)",
                        },
                        "location": {
                            "type": "string",
                            "description": "The location of the event (optional)",
                        }, 
                        "attendees": {
                            "type": "object",
                            "properties": {
                                "email": {"type": "string"}
                            },
                            "required": ["email"],
                            "description": "A list of attendees' email addresses (optional)"
                        },
                    },
                    "required": ["summary", "start_time", "end_time"],
                },
            },
        })
    entry_node = Node(func=tool_use_llm_task, is_llm_call=True, next_nodes={"get_calendar_events": get_calendar_events_node, "create_calendar_event": create_calendar_event_node})

    dag = DAGent(entry_node=entry_node)

    # Execute the DAG
    result = dag.execute("hello world with special")

if __name__ == "__main__":
    main()