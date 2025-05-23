from agentuity import AgentRequest, AgentResponse, AgentContext
from llama_index.core.agent.workflow import AgentWorkflow
from llama_index.llms.openai import OpenAI

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

client = AgentWorkflow.from_tools_or_functions(
    [],
    llm=OpenAI(model="gpt-4o-mini"),
    system_prompt="You are a helpful assistant that provides concise and accurate information.",
)

async def run(request: AgentRequest, response: AgentResponse, context: AgentContext):
    try:
        result = await client.run(await request.data.text() or "Hello, OpenAI")

        return response.text(str(result))
    except Exception as e:
        context.logger.error(f"Error running agent: {e}")

        return response.text("Sorry, there was an error processing your request.")
