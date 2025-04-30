from agentuity import AgentRequest, AgentResponse, AgentContext
from anthropic import AsyncAnthropic

client = AsyncAnthropic()


async def run(request: AgentRequest, response: AgentResponse, context: AgentContext):
    result = await client.messages.create(
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": await request.data.text() or "Hello, Claude",
            }
        ],
        model="claude-3-5-sonnet-latest",
    )
    return response.text(result.content[0].text)
