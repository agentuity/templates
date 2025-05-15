from agentuity import AgentRequest, AgentResponse, AgentContext
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI()


def welcome():  
    return {  
        "welcome": "Welcome to the LangChain Agent with OpenAI! I can help you build powerful language processing chains using LangChain and OpenAI models.",  
        "prompts": [  
            {  
                "data": "Create a summarization chain for a long document",  
                "contentType": "text/plain"  
            },  
            {  
                "data": "How can I use LangChain with vector databases for retrieval?",  
                "contentType": "text/plain"  
            }  
        ]  
    } 

async def run(request: AgentRequest, response: AgentResponse, context: AgentContext):
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an expert in world knowledge and all things in general.",
            ),
            ("user", "{input}"),
        ]
    )
    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser
    result = await chain.ainvoke({"input": await request.data.text() or "Tell me about AI"})

    return response.text(result)
