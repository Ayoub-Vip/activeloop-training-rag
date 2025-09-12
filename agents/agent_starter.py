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
from ..config import DATA_DIR


Settings.embed_model(HuggingFaceInferenceAPIEmbedding(
    model_name="BAAI/bge-small-en-v1.5",
    token=os.getenv("HUGGINGFACE_TOKEN")
))
Settings.llm_model(OpenAI(model="gpt-3.5-turbo"))
load_dotenv(dotenv_path='../')

# def mult(a, b): return a*b these are not well documented 
# def add(a, b): return a+b
def multiply(a: float, b: float) -> float:
    """Multiply two numbers and returns the product"""
    return a * b


def add(a: float, b: float) -> float:
    """Add two numbers and returns the sum"""
    return a + b

async def dangerous_task(ctx: Context) -> str:
    """A dangerous task that requires human confirmation."""

    # emit a waiter event (InputRequiredEvent here)
    # and wait until we see a HumanResponseEvent
    question = "Are you sure you want to proceed? "
    response = await ctx.wait_for_event(
        HumanResponseEvent,
        waiter_id=question,
        waiter_event=InputRequiredEvent(
            prefix=question,
            user_name="Laurie",
        ),
        requirements={"user_name": "Laurie"},
    )

    # act on the input from the event
    if response.response.strip().lower() == "yes":
        return "Dangerous task completed successfully."
    else:
        return "Dangerous task aborted."

func_tools = BaseTool().extend([multiply, add, dangerous_task()])

agent = FunctionAgent(
    name="my first agent",
    description="this agent is a quickstarter example from doc llamaindex.",
    tools=func_tools,
    llm=Settings.llm,
    system_prompt="you are an agent that can multiply and add numbers"
)




handler = agent.run(user_msg="I want to proceed with the dangerous task.")

for event in handler.stream_events():
    if isinstance(event, InputRequiredEvent):
        # capture keyboard input
        response = input(event.prefix)
        # send our response back
        handler.ctx.send_event(
            HumanResponseEvent(
                response=response,
                user_name=event.user_name,
            )
        )

response = handler
print(str(response))


# --- create our specialist agents ------------------------------------------------
research_agent = FunctionAgent(
    name="ResearchAgent",
    description="Search the web and record notes.",
    system_prompt="You are a researcher… hand off to WriteAgent when ready.",
    llm=llm,
    tools=[search_web, record_notes],
    can_handoff_to=["WriteAgent"],
)

write_agent = FunctionAgent(
    name="WriteAgent",
    description="Writes a markdown report from the notes.",
    system_prompt="You are a writer… ask ReviewAgent for feedback when done.",
    llm=llm,
    tools=[write_report],
    can_handoff_to=["ReviewAgent", "ResearchAgent"],
)

review_agent = FunctionAgent(
    name="ReviewAgent",
    description="Reviews a report and gives feedback.",
    system_prompt="You are a reviewer…",  # etc.
    llm=llm,
    tools=[review_report],
    can_handoff_to=["WriteAgent"],
)

# --- wire them together ----------------------------------------------------------
agent_workflow = AgentWorkflow(
    agents=[research_agent, write_agent, review_agent],
    root_agent=research_agent.name,
    initial_state={
        "research_notes": {},
        "report_content": "Not written yet.",
        "review": "Review required.",
    },
)

resp = agent_workflow.run(
    user_msg="Write me a report on the history of the web …"
)
print(resp)