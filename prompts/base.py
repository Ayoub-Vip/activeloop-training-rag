from llama_index.core.prompts import BasePromptTemplate
from abc import ABC, abstractmethod


class BasePrompt(ABC):
    def __init__(self):
        super().__init__()
        self.prompt_tmpl = None