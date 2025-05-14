from openai import AsyncOpenAI
from agentuity import AgentRequest, AgentResponse, AgentContext

client = AsyncOpenAI()

def welcome():  
    return {  
        "welcome": "Welcome to the OpenAI Agent! I can help you interact with OpenAI models.",  
        "prompts": [  
            {  
                "data": "Generate a creative story about a robot learning to paint",  
                "contentType": "text/plain"  
            },  
            {  
                "data": "What capabilities does GPT-4 have?",  
                "contentType": "text/plain"  
            }  
        ]  
    }  

async def run(request: AgentRequest, response: AgentResponse, context: AgentContext):
    chat_completion = await client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a friendly assistant!",
            },
            {
                "role": "user",
                "content": await request.data.text() or "Why is the sky blue?",
            },
        ],
        model="gpt-4o",
    )
    return response.text(chat_completion.choices[0].message.content)
