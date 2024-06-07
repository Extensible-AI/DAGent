from litellm import completion
# For more info: https://litellm.vercel.app/docs/completion/input

def call_llm_tool(model, messages, tools, api_base=None):
# response_format={"type":"json_object"}
    response = completion(
        model=model,
        messages=messages,
        tools=tools,
        api_base=api_base
    )
    return response.choices[0].message
    
