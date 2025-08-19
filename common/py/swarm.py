from agentuity import AgentRequest, AgentResponse, AgentContext
from swarm import Swarm, Agent

# Initialize the Swarm client
client = Swarm()

def welcome():
    return {
        "welcome": "Welcome to the OpenAI Swarm Agent! I can help you build multi-agent orchestration systems with lightweight agent handoffs.",
        "prompts": [
            {
                "data": "Show me how agents can hand off conversations to each other",
                "contentType": "text/plain"
            },
            {
                "data": "What are the best practices for designing multi-agent workflows?",
                "contentType": "text/plain"
            }
        ]
    }

# Helper agent that can handle specialized tasks
def transfer_to_specialist():
    return specialist_agent

# Main conversational agent
main_agent = Agent(
    name="Main Agent",
    instructions="You are a helpful assistant. If the user asks for specialized help or complex analysis, transfer them to the specialist agent using the transfer_to_specialist function.",
    functions=[transfer_to_specialist],
)

# Specialist agent for complex queries
specialist_agent = Agent(
    name="Specialist Agent", 
    instructions="You are a specialist agent with deep expertise. Provide detailed, technical responses and thorough analysis.",
)

async def run(request: AgentRequest, response: AgentResponse, context: AgentContext):
    try:
        user_message = await request.data.text() or "Hello! I'd like to learn about OpenAI Swarm."
        
        # Run the swarm with the main agent
        swarm_response = client.run(
            agent=main_agent,
            messages=[{"role": "user", "content": user_message}],
        )

        # Get the final message from the conversation
        final_message = swarm_response.messages[-1]["content"]
        
        return response.text(final_message)
    except Exception as e:
        context.logger.error(f"Error running Swarm agent: {e}")
        return response.text("Sorry, there was an error processing your request with the Swarm agents.")
