from .state import ResearchAgentState, ResearchAgentSetup
from langchain_core.messages import SystemMessage

def research_setup(state: ResearchAgentSetup):

    user_infos = "Here are the user informations: \n"
    user_infos += f"Tech experience: \n{state['tech_xp']}\n"
    user_infos += f"Actual tech stack: \n{state['actual_tech_stack']}\n"
    user_infos += f"Carrer goals: \n{state['carrer_goals']}\n"
    user_infos += f"Side project goal: \n{state['side_project_goal']}\n"

    system_message = SystemMessage(content=user_infos)

    return {"system_message": system_message}


def research_agent(state: ResearchAgentState):

    
    return state
