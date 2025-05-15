from agentuity import AgentRequest, AgentResponse, AgentContext
from agents.{{ .AgentName | safe_filename }}.crew import MyCrew

def welcome():  
    return {  
        "welcome": "Welcome to the CrewAI Agent! I can help you create and manage AI agent crews for collaborative tasks.",  
        "prompts": [  
            {  
                "data": "Analyze the current trends in renewable energy",  
                "contentType": "text/plain"  
            },  
            {  
                "data": "Research the impact of artificial intelligence on healthcare",  
                "contentType": "text/plain"  
            }  
        ]  
    }  
  

async def run(request: AgentRequest, response: AgentResponse, context: AgentContext):
    inputs = {"topic": await request.data.text() or "AI LLMs"}
    crew = MyCrew().crew()
    result = await crew.kickoff_async(inputs=inputs)
    return response.text(str(result))
