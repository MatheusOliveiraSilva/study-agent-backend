from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, List, Literal
from app.study_plan.agents.research_graph.streaming_utilities import LLMStreamer
from app.study_plan.agents.research_graph.graph import research_graph
from app.study_plan.services.create_final_plan import CreateFinalPlan

router = APIRouter(prefix="/study_plan", tags=["Study Plan"])

class ModelConfig(BaseModel):
    model: str = "o4-mini"
    provider: str = "openai"
    reasoning_effort: Optional[Literal["low", "medium", "high"]] = "low"
    think_mode: Optional[bool] = False
    temperature: Optional[float] = 0
    max_tokens: Optional[int] = 10000

class StudyPlanRequest(BaseModel):
    thread_id: str
    tech_xp: str
    actual_tech_stack: str
    carrer_goals: str
    side_project_goal: str
    llm_config: Optional[ModelConfig] = None
    user_feedback: Optional[str] = None

class FinalPlanRequest(BaseModel):
    study_plan_string: str

@router.post("/generate_study_plan")
def study_plan_stream(
        request: StudyPlanRequest
    ):

    llm_streamer = LLMStreamer()

    # Converter o ModelConfig para dicionário se ele não for None
    llm_config_dict = request.llm_config.dict() if request.llm_config else None
 
    agent_input = {
        "tech_xp": request.tech_xp,
        "actual_tech_stack": request.actual_tech_stack,
        "carrer_goals": request.carrer_goals,
        "side_project_goal": request.side_project_goal,
        "llm_config": llm_config_dict,
        "user_feedback": request.user_feedback
    }

    return StreamingResponse(
        llm_streamer.stream_response(
            agent=research_graph,
            agent_input=agent_input,
            memory_config={"configurable": {"thread_id": request.thread_id}, "recursion_limit": 100}
        ),
        media_type="text/event-stream"
    )


@router.post("/generate_final_plan")
def study_plan_stream(
        request: FinalPlanRequest
    ):

    create_final_plan = CreateFinalPlan(request.study_plan_string)

    return create_final_plan.create_final_plan()



