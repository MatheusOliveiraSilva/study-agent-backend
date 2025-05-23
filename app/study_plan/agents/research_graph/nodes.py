from app.study_plan.agents.research_graph.state import ResearchAgentState
from langchain_core.messages import SystemMessage, HumanMessage
from app.core.llm_config import LLMConfig
from app.study_plan.agents.research_graph.tools import web_search
from app.study_plan.agents.research_graph.prompts import RESEARCH_SYSTEM_PROMPT

def research_setup(state: ResearchAgentState) -> ResearchAgentState:

    user_infos = ""

    if state["user_feedback"]:
        user_infos = f"Feedback do usuário: \n{state['user_feedback']}\n"
    else:
        user_infos = "Aqui estão as informações do usuário: \n"
        user_infos += f"Tech experience: \n{state['tech_xp']}\n"
        user_infos += f"Tech stack atual: \n{state['actual_tech_stack']}\n"
        user_infos += f"Objetivos de carreira: \n{state['carrer_goals']}\n"
        user_infos += f"Objetivo de side project: \n{state['side_project_goal']}\n"
        state["research"] += [HumanMessage(content="Vamos começar a pesquisa.")]

    state["system_message"] = SystemMessage(content=RESEARCH_SYSTEM_PROMPT.format(user_infos=user_infos))

    return state

def research_node(state: ResearchAgentState) -> ResearchAgentState:
    config = LLMConfig(**state["llm_config"])

    llm = config.get_llm()
    llm_with_tools = llm.bind_tools([web_search])

    return {"research": [llm_with_tools.invoke([state["system_message"]] + state["research"])]}