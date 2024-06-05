from litellm import completion
# For more info: https://litellm.vercel.app/docs/completion/input

def call_llm(model, messages, tools, response_format={"type":"json_object"}, api_base=None):
    response = completion(
        model=model,
        messages=messages,
        tools=tools,
        response_format=response_format,
        api_base=api_base
    )
    
