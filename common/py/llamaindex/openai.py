from agentuity import AgentRequest, AgentResponse, AgentContext
from llama_index.llms.openai import OpenAI
from llama_index.core.llms import ChatMessage
import os

# TODO: Add your key via `agentuity env set --secret OPENAI_API_KEY`
# Get your API key here: https://platform.openai.com/settings/organization/api-keys
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable not set.")

client = OpenAI(
    model="gpt-5-mini",
    api_key=api_key
)

def welcome():
    return {
        "welcome": "Welcome to the LlamaIndex Agent with OpenAI! I can help you build AI-powered applications using LlamaIndex and OpenAI models.",
        "prompts": [
            {
                "data": "How do I use LlamaIndex to call OpenAI models?",
                "contentType": "text/plain"
            },
            {
                "data": "What are the best practices for prompt engineering with LlamaIndex?",
                "contentType": "text/plain"
            }
        ]
    }

async def run(request: AgentRequest, response: AgentResponse, context: AgentContext):
    try:
        result = client.chat([
            ChatMessage(
                role="system",
                content="You are a helpful assistant that provides concise and accurate information."
            ),
            ChatMessage(
                role="user",
                content=await request.data.text() or "Hello, OpenAI"
            )
        ])

        return response.text(str(result))
    except Exception as e:
        context.logger.error(f"Error running agent: {e}")

        return response.text("Sorry, there was an error processing your request.")
