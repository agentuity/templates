from agentuity import AgentRequest, AgentResponse, AgentContext  
from agents import Agent, InputGuardrail, GuardrailFunctionOutput, Runner
from pydantic import BaseModel  

class QueryClassification(BaseModel):  
    is_valid: bool  
    category: str
    reasoning: str

# Define the classification agent for input validation
classification_agent = Agent(  
    name="Query Classifier",  
    instructions="Classify user queries and determine if they are valid and what category they belong to.",  
    output_type=QueryClassification,  
)  

# Define specialist agents
general_assistant_agent = Agent(  
    name="General Assistant",  
    handoff_description="General purpose assistant for various queries",  
    instructions="You are a helpful general assistant that can answer a wide variety of questions with accuracy and clarity.",  
)  

technical_agent = Agent(  
    name="Technical Specialist",  
    handoff_description="Technical specialist for programming and technical questions",  
    instructions="You are a technical specialist who helps with programming, software development, and technical problem-solving. Provide detailed explanations and code examples when appropriate.",  
)

# Create guardrail function for input validation
async def query_validation_guardrail(ctx, agent, input_data):  
    result = await Runner.run(classification_agent, input_data, context=ctx)  
    classification = result.final_output_as(QueryClassification)  
    return GuardrailFunctionOutput(  
        output_info=classification,  
        tripwire_triggered=not classification.is_valid,  
    )  

# Main triage agent that routes queries to specialist agents
triage_agent = Agent(  
    name="Triage Agent",  
    instructions="You determine which specialist agent to use based on the user's query. Route technical questions to the Technical Specialist and general questions to the General Assistant.",  
    handoffs=[general_assistant_agent, technical_agent],  
    input_guardrails=[  
        InputGuardrail(guardrail_function=query_validation_guardrail),  
    ],  
)  

def welcome():
    return {
        "welcome": "Welcome to the OpenAI Agents framework! I use multiple specialized agents to handle different types of queries with handoffs and guardrails for better responses.",
        "prompts": [
            {
                "data": "How do I build a REST API with Python?",
                "contentType": "text/plain"
            },
            {
                "data": "What's the weather like today?",
                "contentType": "text/plain"
            },
            {
                "data": "Explain how machine learning works",
                "contentType": "text/plain"
            }
        ]
    }

async def run(request: AgentRequest, response: AgentResponse, context: AgentContext):  
    try:  
        # Extract the user's question from the request  
        user_question = await request.data.text()  
          
        # Log the incoming request  
        context.logger.info("Processing question with OpenAI Agents: %s", user_question)  
          
        # Run the OpenAI Agents workflow  
        result = await Runner.run(triage_agent, user_question, context=context)  
          
        # Log the result  
        context.logger.info("OpenAI Agents workflow completed successfully")  
          
        # Return the response from the OpenAI Agents workflow  
        return response.text(str(result.final_output))  
          
    except Exception as e:  
        context.logger.error("Error in OpenAI Agents workflow: %s", str(e))  
        return response.text(f"Sorry, I encountered an error processing your request: {str(e)}")
