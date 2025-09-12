import os
import asyncio

from typing import Annotated, Optional
from loguru import logger
from dotenv import load_dotenv
from pydantic import Field, PrivateAttr

from llama_index.core.workflow import (
    Workflow,
    step,
    Event,
    StartEvent,
    Checkpoint,
    StopEvent,
    Context
)
from llama_index.core.agent import AgentWorkflow
from llama_index.utils.workflow import draw_all_possible_flows
from llama_index.core.settings import Settings

class MyFirstEvent(Event):
    first_field: int = Field(description="an arbitrary field")
    _private_attr_first: int = PrivateAttr()

class MySecondEvent(Event):
    second_field: int = Field(description="an arbitrary field")
    _private_attr_second: int = PrivateAttr()
    
class BadQueryEvent(Event):
    error_message: str = Field(description="the error code message to be debuged")
    
class LoopEvent(Event):
    loop_output: str
    
class Branch1Event(Event):
    payload: str
    
class Branch2Event(Event):
    payload: str

class ParallelStepAEvent(Event):
    smth: any

class ParallelStepBEvent(Event):
    smth: any
    
class ParallelStepCEvent(Event):
    smth: any
    
class MyFirstWorkflow(Workflow):
    @step
    async def first_step(self, ev: StartEvent) -> MyFirstEvent:
        # Do something here, invoke RAG/LLM/DB....
        
        return MyFirstEvent(first_field=100)
    
    @step
    async def loop(self, ev: MyFirstEvent | LoopEvent) -> MySecondEvent | LoopEvent:
        # print(ev.first_field)
        ...
        bad = True
        if bad:
            return LoopEvent(loop_output="loop again")
        else:
            return MySecondEvent(second_field=1000)
        
    @step
    async def second_step(self, ev: MySecondEvent) -> Branch1Event | Branch2Event:
        
        cond = True
        if cond:
            return Branch1Event("branch 1 is choosen")
        else:
            return Branch2Event("branch 2 is choosen")
        
    @step
    async def third_step(self, ev: Branch1Event | Branch2Event) -> StopEvent:
        print(ev.payload)
        return StopEvent(result="the result of Agent workflow")

    # return BadQueryEvent(error_message="tis is the error message encoutered")
workflow = MyFirstWorkflow()
draw_all_possible_flows(workflow, filename="my_first_workflow.html")


class SubConcurrentWorkflow(MyFirstWorkflow):
    @step
    async def first_step(self, ctx: Context, ev: StartEvent) -> ParallelStepAEvent | ParallelStepBEvent | ParallelStepCEvent:
        ctx.sent_event(ParallelStepAEvent(smth="string A"))
        ctx.sent_event(ParallelStepBEvent(smth="string B"))
        ctx.sent_event(ParallelStepCEvent(smth="string C"))
        
    @step
    async def proceed_to_first_event(self, ctx: Context, ev: ParallelStepAEvent | ParallelStepBEvent | ParallelStepCEvent) -> MyFirstEvent:
        if ctx.collect_events(ev, [ParallelStepAEvent, ParallelStepBEvent, ParallelStepCEvent]) is None:
            return None
        
        return MyFirstEvent()