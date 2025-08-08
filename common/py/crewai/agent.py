from agentuity import AgentRequest, AgentResponse, AgentContext
from agentuity_agents.{{ .AgentName | safe_filename }}.crew import MyCrew

def welcome():
    return {
        "welcome": "Welcome to the CrewAI Agent! I can help you create and manage AI agent crews for collaborative tasks.",
        "prompts": [
            {
                "data": "How do I use CrewAI to create and manage AI agent crews?",
                "contentType": "text/plain"
            },
            {
                "data": "What are the best practices for prompt engineering with CrewAI?",
                "contentType": "text/plain"
            }
        ]
    }

async def run(request: AgentRequest, response: AgentResponse, context: AgentContext):
    try:
        crew = MyCrew().crew()
        inputs = {"topic": await request.data.text() or "AI Agents"}

        result = await crew.kickoff_async(inputs=inputs)

        return response.text(str(result))
    except Exception as e:
        context.logger.error(f"Error running agent: {e}")

        return response.text("Sorry, there was an error processing your request.")
