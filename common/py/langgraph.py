from agentuity import AgentRequest, AgentResponse, AgentContext
from langgraph.graph import MessagesState, StateGraph, END, START
from langgraph.prebuilt import ToolNode
from langchain_core.tools import tool
from langchain_core.messages import AIMessage
from langchain_openai import ChatOpenAI

def welcome():
    return {
        "welcome": "Welcome to the LangGraph Agent! I can help you build stateful AI agents with graph-based workflows and human-in-the-loop controls.",
        "prompts": [
            {
                "data": "How do I create stateful agents with LangGraph workflows?",
                "contentType": "text/plain"
            },
            {
                "data": "What are the advantages of using graph-based agent architectures?",
                "contentType": "text/plain"
            }
        ]
    }

# Define example tools for the LangGraph agent
@tool
def get_info(topic: str) -> str:
    """
    Get information about a specific topic related to LangGraph and agent development.
    
    Args:
        topic (str): The topic to get information about
        
    Returns:
        str: Information about the topic
    """
    info_database = {
        "langgraph": "LangGraph is a framework for building stateful AI agents with graph-based workflows, human-in-the-loop controls, and persistence.",
        "stategraph": "StateGraph is the core component in LangGraph that defines the nodes and edges of your agent workflow.",
        "tools": "Tools in LangGraph are Python functions that agents can call to perform specific actions or retrieve information.",
        "workflows": "Workflows in LangGraph are defined as graphs with nodes (functions) and edges (control flow) that enable complex agent behavior."
    }
    
    topic_lower = topic.lower()
    for key, value in info_database.items():
        if key in topic_lower:
            return value
    
    return f"LangGraph is a powerful framework for building stateful AI agents. It provides graph-based workflows, tool integration, and human-in-the-loop controls for reliable agent development."

# List of available tools
tools = [get_info]

# Initialize the LLM and bind tools
model = ChatOpenAI(model="gpt-5-mini", temperature=0).bind_tools(tools)
tool_node = ToolNode(tools)

def call_model(state: MessagesState) -> dict:
    """Node to call the agent model"""
    messages = state["messages"]
    response = model.invoke(messages)
    return {"messages": [response]}

def should_continue(state: MessagesState) -> str:
    """Determine whether to call tools or end the workflow"""
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    return END

# Build the StateGraph
workflow = StateGraph(MessagesState)
workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)

workflow.add_edge(START, "agent")
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "tools": "tools",
        END: END,
    },
)
workflow.add_edge("tools", "agent")

# Compile the graph
agent_graph = workflow.compile()

async def run(request: AgentRequest, response: AgentResponse, context: AgentContext):
    try:
        user_message = await request.data.text() or "Tell me about LangGraph and how it helps build stateful AI agents."
        
        # Create initial state with user message
        initial_state = {"messages": [("human", user_message)]}
        
        # Run the LangGraph workflow
        final_state = None
        for chunk in agent_graph.stream(initial_state, stream_mode="values"):
            if "messages" in chunk and chunk["messages"]:
                final_state = chunk
        
        # Extract the final response
        if final_state and "messages" in final_state and final_state["messages"]:
            # Get the last AI message
            for message in reversed(final_state["messages"]):
                if isinstance(message, AIMessage):
                    return response.text(message.content)
        
        return response.text("I'd be happy to help you learn about LangGraph and building stateful AI agents! Please ask me about graph-based workflows, tools, or agent architecture.")
        
    except Exception as e:
        context.logger.error(f"Error running LangGraph agent: {e}")
        return response.text("Sorry, there was an error processing your request with the LangGraph agent.")
