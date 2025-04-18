from typing import TypedDict, Annotated, List
from langgraph.graph import add_messages

class ResearchAgentInput(TypedDict):
    tech_xp: str
    actual_tech_stack: str
    carrer_goals: str
    side_project_goal: str

class ResearchAgentOutput(TypedDict):
    research_output: Annotated[list, add_messages]

class ResearchAgentState(TypedDict):
    research_context: List[str]