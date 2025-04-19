from typing import TypedDict, Annotated, List
from langgraph.graph import add_messages
from langchain_core.messages import SystemMessage

class ResearchAgentState(TypedDict):
    tech_xp: str
    actual_tech_stack: str
    carrer_goals: str
    side_project_goal: str

    system_message: SystemMessage
    research: Annotated[list, add_messages]
    research_context: List[str]