#!/bin/bash

curl -X POST http://localhost:8000/study_plan/generate_study_plan \
  -H "Content-Type: application/json" \
  -d '{
    "thread_id": "test123",
    "tech_xp": "2 anos como desenvolvedor backend",
    "actual_tech_stack": "Python, Langchain, LangGraph, SQL, Git",
    "carrer_goals": "Quero virar um AI Engineer, e internacionalizar minha carreira, ganhando em dolar",
    "side_project_goal": "Fazer um RAG chatbot com possibilidade de envio de documentos e imagens, monitorar tudo.",
    "llm_config": {
      "model": "o4-mini",
      "provider": "openai",
      "reasoning_effort": "high",
      "max_tokens": 10000
    }
  }' 