from agentuity import AgentRequest, AgentResponse, AgentContext
from haystack.components.generators.chat import OpenAIChatGenerator
from haystack.dataclasses import ChatMessage

def welcome():
    return {
        "welcome": "Welcome to the Haystack Agent! I can help you build AI-powered search applications with RAG capabilities and semantic search.",
        "prompts": [
            {
                "data": "How does Retrieval Augmented Generation work in Haystack?",
                "contentType": "text/plain"
            },
            {
                "data": "What are the advantages of using semantic search over traditional keyword search?",
                "contentType": "text/plain"
            }
        ]
    }

async def run(request: AgentRequest, response: AgentResponse, context: AgentContext):
    try:
        user_message = await request.data.text() or "Tell me about Haystack and how RAG works."
        
        # Create a simple chat generator using Haystack
        chat_generator = OpenAIChatGenerator(model="gpt-5-mini")
        
        # Create system message with Haystack expertise
        messages = [
            ChatMessage.from_system("You are an expert in Haystack, the Python framework for building AI-powered search applications. You specialize in explaining RAG (Retrieval Augmented Generation), semantic search, document stores, pipelines, and how to build production-ready search applications. Provide detailed, practical information."),
            ChatMessage.from_user(user_message)
        ]
        
        # Generate response
        result = chat_generator.run(messages=messages)
        
        # Extract the response
        if result and "replies" in result and result["replies"]:
            answer = result["replies"][0].text
            return response.text(answer)
        else:
            return response.text("I'd be happy to help you with Haystack and RAG applications! Could you please rephrase your question?")
            
    except Exception as e:
        context.logger.error(f"Error running Haystack agent: {e}")
        return response.text("Sorry, there was an error processing your request with the Haystack system.")
