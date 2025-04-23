from typing import List
from pydantic import BaseModel, Field
from app.core.llm_config import LLMConfig

class MicroTopic(BaseModel):
    easy_milestone: str = Field(..., description="Entrega fácil")
    medium_milestone: str = Field(..., description="Entrega média")
    hard_milestone: str = Field(..., description="Entrega difícil")
    description: str = Field(..., description="Descrição do tópico")
    time_to_study: int = Field(..., description="Tempo estimado para estudar o tópico.")
    
class MacroTopic(BaseModel):
    name: str = Field(..., description="Nome do tópico")
    description: str = Field(..., description="Descrição do tópico")
    time_to_study: int = Field(..., description="Tempo estimado para estudar o tópico.")
    micro_topics: List[MicroTopic] = Field(..., description="Tópicos menores de estudo que compõem o tópico principal.")

class StudyPlan(BaseModel):
    macro_topics: List[MacroTopic] = Field(..., description="Tópicos principais de estudo, cada um tem tópicos menores de estudo, e micro entregas para o usuário exercitar o que aprendeu.")

class CreateFinalPlan:
    def __init__(self, study_plan_string: str):
        self.study_plan_string = study_plan_string
        self.prompt = """
Você é um especialista em planejamento de estudo.

Vou te dar um plano de estudo e você deve ajustar o plano no formato de output que eu vou te dar.

É importante que você complete cada milestone, se no plano original não tiver todas milestones, adicione.

Input do usuário:
{study_plan_string}
"""

    def create_final_plan(self):
        llm_config = LLMConfig(
            provider="openai",
            model="gpt-4.1-nano",
            max_tokens=10000
        )

        prompt = self.prompt.format(study_plan_string=self.study_plan_string)

        return llm_config.get_llm().with_structured_output(StudyPlan).invoke(prompt)
