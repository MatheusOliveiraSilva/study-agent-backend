# tests/core/test_llm_config.py
from langchain_openai import AzureOpenAI
from app.core.llm_config import LLMConfig

def test_get_azure_llm_default():
    """Testa se get_llm chama AzureOpenAI com defaults quando provider='azure'."""
    config = LLMConfig(provider="azure")
    llm = config.get_llm()

    assert isinstance(llm, AzureOpenAI)
    assert llm.model_name == config.DEFAULT_AZURE_MODEL
    assert llm.temperature == config.DEFAULT_TEMPERATURE

def test_get_azure_llm_specific_model():
    """Testa se get_llm chama AzureOpenAI com modelo específico quando provider='azure'."""
    config = LLMConfig(provider="azure")
    llm = config.get_llm(model="o3-mini")

    assert isinstance(llm, AzureOpenAI)
    assert llm.model_name == "o3-mini"

def test_get_azure_llm_with_kwargs():
    """Testa se get_llm chama AzureOpenAI com modelo específico quando provider='azure'."""
    config = LLMConfig(provider="azure")
    llm = config.get_llm(model="o3-mini", temperature=0.5, max_tokens=100)

    assert isinstance(llm, AzureOpenAI)
    assert llm.model_name == "o3-mini"
    assert llm.temperature == 1 # o3-mini requires temperature to be 1, test with we correct temperature
    assert llm.max_tokens == 100