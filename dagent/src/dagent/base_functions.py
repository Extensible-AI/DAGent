from litellm import completion
from openai import OpenAI
# For more info: https://litellm.vercel.app/docs/completion/input

client = OpenAI()

def call_llm_tool(model, messages, tools, api_base=None, **kwargs):
    response = completion(
        model=model,
        messages=messages,
        tools=tools,
        api_base=api_base
    )
    return response.choices[0].message
    

def create_tool_desc(model, function_desc):
    example = {
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
            }
    }
    messages = [{"role": "user", "content": "Create a json for the attached function: {} using the following pattern for the json: {}. Don't add anything extra".format(function_desc, example)}]
    response = client.chat.completions.create(
        model=model,
        response_format={"type":"json_object"},
        messages=messages
    )
    return response.choices[0].message.content
