from litellm import acompletion
from agentuity import AgentRequest, AgentResponse, AgentContext

def welcome():  
    return {  
        "welcome": "Welcome to the LiteLLM Agent! I can help you interact with various LLM providers through a unified interface.",  
        "prompts": [  
            {  
                "data": "Generate a response using OpenAI's GPT-4 model",  
                "contentType": "text/plain"  
            },  
            {  
                "data": "What LLM providers does LiteLLM support?",  
                "contentType": "text/plain"  
            }  
        ]  
    }  

async def run(request: AgentRequest, response: AgentResponse, context: AgentContext):
    messages = [{"content": await request.data.text() or "Hello, how are you?", "role": "user"}]
    result = await acompletion(model="openai/gpt-4o", messages=messages)
    return response.text(result.choices[0].message.content)

