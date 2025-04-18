import os
from langchain_openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

class LLMConfig:
    """
    LLMConfig is a class that configures the LLM for the application.
    """

    def __init__(self, provider=None, **kwargs):
        # Store config from environment
        self.AZURE_OPENAI_BASE_URL = os.environ.get("AZURE_OPENAI_BASE_URL")
        self.OPENAI_API_KEY = os.environ.get("AZURE_OPENAI_API_KEY")
        self.OPENAI_API_VERSION = os.environ.get("OPENAI_API_VERSION")

        self.DEFAULT_PROVIDER = "azure"
        self.DEFAULT_AZURE_MODEL = "gpt-4o"
        self.DEFAULT_BEDROCK_MODEL = "claude-3-5-sonnet"
        self.DEFAULT_TEMPERATURE = 0

        # Store provider and kwargs
        self.provider = provider if provider is not None else self.DEFAULT_PROVIDER
        self.kwargs = kwargs

    def get_llm(self, **kwargs):
        # Use provider from initialization
        provider = self.provider
        
        # Combine kwargs from init and those passed to get_llm
        combined_kwargs = {**self.kwargs, **kwargs}
        
        if provider == "azure":
            return self.get_azure_llm(**combined_kwargs)
        elif provider == "bedrock":
            return self.get_bedrock_llm(**combined_kwargs)
        else:
            raise ValueError(f"Provider {provider} not supported")

    def get_azure_llm(self, **kwargs):
        """Configures and returns an AzureOpenAI instance."""
        # Determine model based on received kwargs or default
        model = kwargs.get("model", self.DEFAULT_AZURE_MODEL)

        # Build the arguments dictionary for AzureOpenAI constructor
        final_args_for_azure = {
            # Add credentials from stored env vars
            "azure_endpoint": self.AZURE_OPENAI_BASE_URL,
            "openai_api_key": self.OPENAI_API_KEY,
            "api_version": self.OPENAI_API_VERSION,
            "model": model,
            # Pass through any *other* kwargs provided
            **kwargs
        }

        # Specific adjustments can be made here before initializing
        # Example: Adjust temperature specifically for 'o3'/'o1' models (need to be 1)
        if model.startswith("o3") or model.startswith("o1"):
            final_args_for_azure["temperature"] = 1
        else:
            final_args_for_azure["temperature"] = kwargs.get("temperature", self.DEFAULT_TEMPERATURE)

        return AzureOpenAI(**final_args_for_azure)

    def get_bedrock_llm(self, **kwargs):
        pass
