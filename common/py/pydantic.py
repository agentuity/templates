from agentuity import AgentRequest, AgentResponse, AgentContext
from pydantic_ai import Agent

client = Agent("openai:gpt-4o-mini")

def welcome():
    return {
        "welcome": "Welcome to the Pydantic Python Agent! I can help you build AI-powered applications using Pydantic.",
        "prompts": [
            {
                "data": "How do I use Pydantic to call OpenAI models?",
                "contentType": "text/plain"
            },
            {
                "data": "What are the best practices for prompt engineering with Pydantic?",
                "contentType": "text/plain"
            }
        ]
    }

async def run(request: AgentRequest, response: AgentResponse, context: AgentContext):
    try:
        result = await client.run(await request.data.text() or "Hello, PydanticAI")

        return response.text(result.output)
    except Exception as e:
        context.logger.error(f"Error running agent: {e}")

        return response.text("Sorry, there was an error processing your request.")
