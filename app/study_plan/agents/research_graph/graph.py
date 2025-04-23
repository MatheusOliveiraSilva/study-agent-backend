from langgraph.prebuilt import tools_condition, ToolNode
from langgraph.graph import START, StateGraph
from langgraph.checkpoint.memory import MemorySaver
from app.study_plan.agents.research_graph.nodes import research_node, research_setup
from app.study_plan.agents.research_graph.state import ResearchAgentState
from app.study_plan.agents.research_graph.tools import web_search   

TOOLS = [web_search]    

# Build graph
builder = StateGraph(ResearchAgentState) 
builder.add_node("research_setup", research_setup)
builder.add_node("research_node", research_node)
builder.add_node("tools", ToolNode(TOOLS, messages_key="research"))
builder.add_edge(START, "research_setup")
builder.add_edge("research_setup", "research_node")
builder.add_conditional_edges(
    "research_node",
    lambda state: tools_condition(state, messages_key="research"),
)
builder.add_edge("tools", "research_node")

# Compile graph
research_graph = builder.compile(checkpointer=MemorySaver())

if __name__ == "__main__":

    # Test graph
    response = research_graph.invoke(
        {
            "tech_xp": "2 anos como desenvolvedor backend", 
            "actual_tech_stack": "Python, Langchain, LangGraph, SQL, Git", 
            "carrer_goals": "Quero virar um AI Engineer, e internacionalizar minha carreira, ganhando em dolar", 
            "side_project_goal": "Fazer um RAG chatbot com possibilidade de envio de documentos e imagens, monitorar tudo."
        }
    )

    print(response)