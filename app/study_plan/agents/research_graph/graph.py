
from langgraph.prebuilt import tools_condition, ToolNode
from langgraph.graph import START, StateGraph, MessagesState
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from .nodes import research_agent
from .state import ResearchAgentState

TOOLS = []
memory = MemorySaver()

# Build graph
builder = StateGraph(ResearchAgentState)
builder.add_node("research_agent", research_agent)
builder.add_node("tools", ToolNode(TOOLS))
builder.add_edge(START, "research_agent")
builder.add_conditional_edges(
    "research_agent",
    # If the latest message (result) from assistant is a tool call -> tools_condition routes to tools (continue to websearch)
    # If the latest message (result) from assistant is a not a tool call -> tools_condition routes to END
    tools_condition,
)
builder.add_edge("tools", "research_agent")

# Compile graph
graph = builder.compile(checkpointer=memory)