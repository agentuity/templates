import random
from pydantic_ai import Agent, RunContext
from agentuity import AgentRequest, AgentResponse, AgentContext


def welcome():
    return {
        "welcome": "Welcome to the Pydantic Agent! I can help you interact with spinning the roulette wheel.",
        "prompts": [
            {
                "data": "Put my money on square eighteen",
                "contentType": "text/plain",
            },
            {
                "data": "I bet five is the winner",
                "contentType": "text/plain",
            },
        ],
    }


# Example taken from: https://ai.pydantic.dev/agents/#introduction

# The pydantic agent
roulette_agent = Agent(
    "openai:gpt-4o",
    deps_type=int,
    output_type=str,
    system_prompt=(
        "Use the `roulette_wheel` function to see if the "
        "customer has won based on the number they provide."
    ),
)


# A tool for the pydantic agent
@roulette_agent.tool
async def roulette_wheel(ctx: RunContext[int], square: int) -> str:
    """check if the square is a winner"""
    return "winner" if square == ctx.deps else "loser"


# The Agentuity agent handler
async def run(request: AgentRequest, response: AgentResponse, context: AgentContext):
    # Spin that wheel!
    success_number = random.randint(0, 20)

    # Pull out the user query from the request
    user_query = await request.data.text()
    if not user_query:
        user_query = str(random.randint(0, 20))

    context.logger.info(
        "User query: %s, Winning number: %s", user_query, success_number
    )

    try:
        context.logger.info(
            "Calling PydanticAI roulette agent with query: '%s' and deps: %s",
            user_query,
            success_number,
        )

        pydantic_ai_result = await roulette_agent.run(user_query, deps=success_number)
        raw = pydantic_ai_result.output
        success = "winner" in raw
        context.logger.info("Roulette success: %s => %d", success, success_number)

        return response.json(
            {
                "success": success,
                "result": pydantic_ai_result.output,
                "query": user_query,
                "success_number": success_number,
            }
        )

    except Exception as e:
        context.logger.error("Error running PydanticAI agent: %s", e)
        return response.json({"error": str(e)})
