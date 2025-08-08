from agentuity import AgentRequest, AgentResponse, AgentContext
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

client = ChatOpenAI(model="gpt-5-mini")

def welcome():
    return {
        "welcome": "Welcome to the LangChain Agent with OpenAI! I can help you build AI-powered applications using LangChain and OpenAI models.",
        "prompts": [
            {
                "data": "How do I use LangChain to call OpenAI models?",
                "contentType": "text/plain"
            },
            {
                "data": "What are the best practices for prompt engineering with LangChain?",
                "contentType": "text/plain"
            }
        ]
    }

async def run(request: AgentRequest, response: AgentResponse, context: AgentContext):
    try:
        prompt = ChatPromptTemplate.from_messages(
                [
                    (
                    "system",
                    "You are a helpful assistant that provides concise and accurate information.",
                ),
                ("user", "{input}"),
            ]
        )
        output_parser = StrOutputParser()
        chain = prompt | client | output_parser

        result = await chain.ainvoke({"input": await request.data.text() or "Tell me about AI"})

        return response.text(result)
    except Exception as e:
        context.logger.error(f"Error running agent: {e}")

        return response.text("Sorry, there was an error processing your request.")
