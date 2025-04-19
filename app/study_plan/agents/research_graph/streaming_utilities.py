import json
from typing import Dict, Any, Generator

class LLMStreamer:
    """
    Class to manage streaming of LLM responses.
    Supports different providers and response formats.
    """
    
    def stream_response(
        self,
        agent,
        agent_input: Dict[str, Any] = None,
        memory_config: Dict[str, Any] = None,
    ) -> Generator[str, None, None]:
        """
        Stream the response from the agent.
        """
        
        if agent_input["llm_config"]["provider"] == "openai":
            return self.openai_stream(agent, agent_input, memory_config)
        else:
            raise ValueError(f"Provider {agent_input['llm_config']['provider']} not supported")
    
    @staticmethod
    def openai_stream(agent, agent_input, memory_config):
        """
        Stream the response from the agent using OpenAI models output format.
        """

        for chunk, meta in agent.stream(
                agent_input, 
                stream_mode="messages",
                config=memory_config
            ):
            
            yield chunk.content
