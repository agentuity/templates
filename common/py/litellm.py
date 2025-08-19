from agentuity import AgentRequest, AgentResponse, AgentContext
from litellm import acompletion

def welcome():
    return {
        "welcome": "Welcome to the LiteLLM Agent! I can help you interact with various LLM providers through a unified interface.",
        "prompts": [
            {
                "data": "How do I implement streaming responses with OpenAI models?",
                "contentType": "text/plain"
            },
            {
                "data": "What LLM providers does LiteLLM support?",
                "contentType": "text/plain"
            }
        ]
    }

async def run(request: AgentRequest, response: AgentResponse, context: AgentContext):
    messages = [{
        "role": "user",
        "content": await request.data.text() or "Hello, LiteLLM",
    }]

    try:
        result = await acompletion(model="openai/gpt-5-mini", messages=messages)

        return response.text(result.choices[0].message.content)
    except Exception as e:
        context.logger.error(f"Error running agent: {e}")

        return response.text("Sorry, there was an error processing your request.")

