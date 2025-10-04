from agentuity import AgentRequest, AgentResponse, AgentContext
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken
from autogen_ext.models.openai import OpenAIChatCompletionClient


def welcome():
    return {
        "welcome": "Welcome to the Microsoft AutoGen Agent! I can help you build multi-agent conversational AI applications with collaborative workflows.",
        "prompts": [
            {
                "data": "Show me how multiple agents can collaborate on a complex task",
                "contentType": "text/plain",
            },
            {
                "data": "What are the advantages of using AutoGen for multi-agent systems?",
                "contentType": "text/plain",
            },
        ],
    }


async def run(request: AgentRequest, response: AgentResponse, context: AgentContext):
    try:
        user_message = (
            await request.data.text()
            or "Hello! Tell me about Microsoft AutoGen and how agents collaborate."
        )

        # Create model client
        model_client = OpenAIChatCompletionClient(model="gpt-4o-mini")

        # Create an AssistantAgent with OpenAI model
        assistant = AssistantAgent(
            name="assistant",
            model_client=model_client,
            system_message="You are a helpful AI assistant specializing in multi-agent systems and collaborative AI workflows. Provide detailed, informative responses about how agents can work together to solve complex problems.",
        )

        # Create a message from the user
        message = TextMessage(content=user_message, source="user")
        cancellation_token = CancellationToken()

        # Send message to assistant and get response
        agent_response = await assistant.on_messages([message], cancellation_token)

        # Close the model client connection
        await model_client.close()

        # Extract the response text
        response_text = agent_response.chat_message.content

        return response.text(response_text)

    except Exception as e:
        context.logger.error(f"Error running AutoGen agent: {e}")
        return response.text(
            "Sorry, there was an error processing your request with the AutoGen agents."
        )
