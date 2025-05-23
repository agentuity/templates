from agentuity import AgentRequest, AgentResponse, AgentContext
from google import genai
import os

# TODO: Add your key via `agentuity env set --secret GOOGLE_API_KEY`
# Get your API key here: https://aistudio.google.com/apikey
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("GOOGLE_API_KEY environment variable not set.")

client = genai.Client(api_key=api_key)

def welcome():
    return {
        "welcome": "Welcome to the Google AI Python Agent! I can help you build AI-powered applications using Gemini models.",
        "prompts": [
            {
                "data": "How do I implement streaming responses with Gemini models?",
                "contentType": "text/plain"
            },
            {
                "data": "What are the best practices for prompt engineering with Gemini?",
                "contentType": "text/plain"
            }
        ]
    }

async def run(request: AgentRequest, response: AgentResponse, context: AgentContext):
    try:
        result = client.models.generate_content(
            model="gemini-2.0-flash",
            contents= await request.data.text() or "Hello, Gemini"
        )

        return response.text(result.text)
    except Exception as e:
        context.logger.error(f"Error running agent: {e}")

        return response.text("Sorry, there was an error processing your request.")