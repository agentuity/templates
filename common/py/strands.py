from agentuity import AgentRequest, AgentResponse, AgentContext
from strands import Agent, tool
from strands.models.openai import OpenAIModel
from strands_tools import calculator, current_time

def welcome():
    return {
        "welcome": "Welcome to the AWS Strands Agent! I can help you build model-driven AI agents with tool integration and AWS capabilities.",
        "prompts": [
            {
                "data": "Show me how to use tools with AWS Strands agents",
                "contentType": "text/plain"
            },
            {
                "data": "What are the advantages of using AWS Strands for agent development?",
                "contentType": "text/plain"
            }
        ]
    }

# Define a custom tool using the @tool decorator
@tool
def text_analyzer(text: str) -> dict:
    """
    Analyze text and return basic statistics.
    
    Args:
        text (str): The input text to analyze
        
    Returns:
        dict: A dictionary containing text statistics
    """
    if not isinstance(text, str):
        return {"error": "Input must be a string"}
    
    words = text.split()
    sentences = text.split('.')
    
    return {
        "character_count": len(text),
        "word_count": len(words),
        "sentence_count": len([s for s in sentences if s.strip()]),
        "average_word_length": sum(len(word) for word in words) / len(words) if words else 0
    }

async def run(request: AgentRequest, response: AgentResponse, context: AgentContext):
    try:
        user_message = await request.data.text() or "Tell me about AWS Strands and how agents work with tools."
        
        # Create OpenAI model for Strands
        openai_model = OpenAIModel(model_id="gpt-5-mini")
        
        # Create a Strands agent with tools and OpenAI model
        agent = Agent(
            tools=[calculator, current_time, text_analyzer],
            model=openai_model,
            system_prompt="You are an expert in AWS Strands, a model-driven AI agent framework. You help users understand how to build agents with tool integration, AWS capabilities, and production deployment. Provide practical, detailed information about agent development."
        )
        
        # Process the user message with the Strands agent
        agent_response = agent(user_message)
        
        return response.text(str(agent_response))
        
    except Exception as e:
        context.logger.error(f"Error running Strands agent: {e}")
        return response.text("Sorry, there was an error processing your request with the AWS Strands agent.")
