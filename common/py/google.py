from google import genai
from agentuity import AgentRequest, AgentResponse, AgentContext
import os

# Get your API key here: https://aistudio.google.com/apikey
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY environment variable not set.")

client = genai.Client(api_key=api_key)

def welcome():  
    return {  
        "welcome": "Welcome to the Google AI Agent! I can help you interact with Gemini models for natural language tasks.",  
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
    
    chat_completion = client.models.generate_content(
        model="gemini-2.0-flash", contents= await request.data.text() or "Why is the sky blue?"
    )
    
    return response.text(chat_completion.text)