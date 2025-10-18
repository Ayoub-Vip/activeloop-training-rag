import os
import asyncio
import chromadb
import wandb

from pathlib import Path
from loguru import logger
from dotenv import load_dotenv

from llama_index.core import download_loader
from llama_index.core import Settings
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.huggingface_api import HuggingFaceInferenceAPIEmbedding
from llama_index.core.settings import Settings
from llama_index.core.agent.workflow import BaseWorkflowAgent, FunctionAgent, AgentWorkflow
from llama_index.core.tools import BaseTool
from llama_index.tools.tavily_research import TavilyToolSpec
from llama_index.core.agent.workflow import AgentStream, AgentInput
from llama_index.core.workflow import (
    InputRequiredEvent,
    HumanResponseEvent,
    Context
)

from ..agents.base import Agent
from ..prompts.extract_output import ExtractorPrompt
from ..pydantics.structured_output import get_output_cls
from ..pydantics import doc_classes
from llama_index.core.prompts import RichPromptTemplate

from ..config import DATA_DIR

class ExtractorAgent(FunctionAgent):
    def __init__(self, doc_type, doc_class):
        prompt_tmplt_str = ExtractorPrompt().prompt_tmplt
        var_map_prompt = {
            "doc_type": doc_type,
            "doc_class": doc_class
        }
        prompt = RichPromptTemplate(
            template_str=prompt_tmplt_str,
            template_var_mappings=var_map_prompt
        )
        output_cls = get_output_cls(doc_class)
        

        super().__init__(
            name="document extractor agent",
            description="this agent extracts informations",
            state_prompt=prompt,
            output_cls=output_cls
        )
        