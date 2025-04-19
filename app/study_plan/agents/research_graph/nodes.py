from app.study_plan.agents.research_graph.state import ResearchAgentState
from langchain_core.messages import SystemMessage, HumanMessage
from app.core.llm_config import LLMConfig
from app.study_plan.agents.research_graph.tools import web_search
from app.study_plan.agents.research_graph.prompts import RESEARCH_SYSTEM_PROMPT

def research_setup(state: ResearchAgentState) -> ResearchAgentState:

    user_infos = "Aqui estão as informações do usuário: \n"
    user_infos += f"Tech experience: \n{state['tech_xp']}\n"
    user_infos += f"Tech stack atual: \n{state['actual_tech_stack']}\n"
    user_infos += f"Objetivos de carreira: \n{state['carrer_goals']}\n"
    user_infos += f"Objetivo de side project: \n{state['side_project_goal']}\n"

    state["system_message"] = SystemMessage(content=RESEARCH_SYSTEM_PROMPT.format(user_infos=user_infos))
    state["research"] = [HumanMessage(content="Vamos começar a pesquisa.")]

    return state

# RESEARCH_LLM_CONFIG = LLMConfig(
#     provider="anthropic", 
#     model="claude-3-7-sonnet-latest",
#     temperature=1,
#     max_tokens=10000,
#     thinking={"type": "enabled", "budget_tokens": 5000}
# )

RESEARCH_LLM_CONFIG = LLMConfig(
    provider="openai",
    model="o4-mini",
    reasoning_effort="high",
)

def research_node(state: ResearchAgentState) -> ResearchAgentState:

    llm = RESEARCH_LLM_CONFIG.get_llm()
    llm_with_tools = llm.bind_tools([web_search])

    return {"research": [llm_with_tools.invoke([state["system_message"]] + state["research"])]}

