from abc import ABC, abstractmethod
from llama_index.core.agent.workflow import BaseWorkflowAgent

class Agent(ABC):
    def __init__(
        self,
        name,
        llm,
        prompt,
        
        ):
        self._agent = BaseWorkflowAgent()