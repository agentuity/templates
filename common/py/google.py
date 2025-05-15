from google import genai
from agentuity import AgentRequest, AgentResponse, AgentContext
import os

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY environment variable not set.")

client = genai.Client(api_key=api_key)


async def run(request: AgentRequest, response: AgentResponse, context: AgentContext):
    
    chat_completion = client.models.generate_content(
        model="gemini-2.0-flash", contents= await request.data.text() or "Why is the sky blue?"
    )
    
    return response.text(chat_completion.text)