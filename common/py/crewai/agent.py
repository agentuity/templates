from agentuity import AgentRequest, AgentResponse, AgentContext
import os
import sys

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from crew import MyCrew

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
