from agentuity import AgentRequest, AgentResponse, AgentContext
from praisonaiagents import Agent, PraisonAIAgents
import asyncio

def welcome():
    return {
        "welcome": "Welcome to the Praison AI Agent! I can help you build production-ready multi-AI agent systems with self-reflection capabilities.",
        "prompts": [
            {
                "data": "How do I create multi-agent systems with Praison AI?",
                "contentType": "text/plain"
            },
            {
                "data": "What are the self-reflection capabilities of Praison AI agents?",
                "contentType": "text/plain"
            }
        ]
    }

async def run(request: AgentRequest, response: AgentResponse, context: AgentContext):
    try:
        user_message = await request.data.text() or "Tell me about Praison AI and how it helps build multi-agent systems."
        
        # Create a Praison AI agent with expertise in the framework
        agent = Agent(
            instructions="""You are an expert in Praison AI, a production-ready framework for creating multi-AI agent systems. 
            You specialize in explaining self-reflection capabilities, multi-agent coordination, CrewAI and AG2 integration, 
            low-code solutions, and building complex LLM systems. Provide detailed, practical information about Praison AI 
            development including code examples when appropriate."""
        )
        
        # Start the agent with the user's message
        # Note: agent.start() is typically synchronous in Praison AI
        result = await asyncio.to_thread(agent.start, user_message)
        
        # Extract response - Praison AI agents typically return the result directly
        if result:
            return response.text(str(result))
        else:
            return response.text("I'd be happy to help you with Praison AI multi-agent systems! Could you please provide more details about what you'd like to know?")
            
    except Exception as e:
        context.logger.error(f"Error running Praison AI agent: {e}")
        return response.text("Sorry, there was an error processing your request with the Praison AI agent.")
