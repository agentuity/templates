from agentuity import AgentRequest, AgentResponse, AgentContext
from agents.{{ .AgentName | safe_filename }}.crew import MyCrew


async def run(request: AgentRequest, response: AgentResponse, context: AgentContext):
    inputs = {"topic": request.data.text or "AI LLMs"}
    crew = MyCrew().crew()
    result = await crew.akickoff(inputs=inputs)
    return response.text(str(result))
