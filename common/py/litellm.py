from litellm import acompletion
from agentuity import AgentRequest, AgentResponse, AgentContext


async def run(request: AgentRequest, response: AgentResponse, context: AgentContext):
    messages = [{"content": request.data.text or "Hello, how are you?", "role": "user"}]
    result = await acompletion(model="openai/gpt-4o", messages=messages)
    return response.text(result.choices[0].message.content)
