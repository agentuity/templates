from agentuity import AgentRequest, AgentResponse, AgentContext
from anthropic import AsyncAnthropic

client = AsyncAnthropic()

def welcome():  
    return {  
        "welcome": "Welcome to the Anthropic Agent! I can help you interact with Claude models for natural language tasks.",  
        "prompts": [  
            {  
                "data": "Write a creative story about a journey through time",  
                "contentType": "text/plain"  
            },  
            {  
                "data": "Explain quantum computing to a high school student",  
                "contentType": "text/plain"  
            }  
        ]  
    }

async def run(request: AgentRequest, response: AgentResponse, context: AgentContext):
    result = await client.messages.create(
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": await request.data.text() or "Hello, Claude",
            }
        ],
        model="claude-3-5-sonnet-latest",
    )
    return response.text(result.content[0].text)
