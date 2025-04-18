from typing import TypedDict, Annotated, List
from langgraph.graph import add_messages
from langchain_core.messages import SystemMessage
class ResearchAgentSetup(TypedDict):
    tech_xp: str
    actual_tech_stack: str
    carrer_goals: str
    side_project_goal: str

class ResearchAgentState(TypedDict):
    system_message: SystemMessage
    research_output: Annotated[list, add_messages]
    research_context: List[str]