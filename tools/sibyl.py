

import os
import sqlite3
from typing import Tuple, Any, List
from langchain_core.outputs import LLMResult
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_community.cache import SQLiteCache
from langchain_core.callbacks import BaseCallbackHandler
from utils.browser_utils import SimpleTextBrowser
from autogen.code_utils import execute_code
import autogen
from autogen.agentchat.contrib.society_of_mind_agent import SocietyOfMindAgent

MODEL = 'gpt-4o'
DATA_NAME = '2023_level1'
SPLIT = 'validation'
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_API_BASE = os.getenv('OPENAI_API_BASE')
BING_API_KEY = os.getenv('BING_API_KEY')

class LLMCallbackHandler(BaseCallbackHandler):
    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> Any:
        print(f"LLM response: {response}")

class Answer(BaseModel):
    reason: str = Field(description="Step by step reasoning")
    answer: str = Field(description="The answer to the question")

class StepNote(BaseModel):
    snippets: List[str] = Field(description="Snippets used to answer the question, each less than 1000 characters")
    plan: str = Field(description="Plan for the next step")

class ToolChoice(BaseModel):
    reason: str = Field(description="Step by step reasoning")
    tool: str = Field(description="The tool to use")
    tool_args: dict = Field(description="The arguments to pass to the tool")

class ImproveCode(BaseModel):
    reason: str = Field(description="Step by step reasoning on how to improve the code")
    improved_code: str = Field(description="The improved code")

with open("prompts/format_answer.txt") as f:
    FORMAT_ANSWER_PROMPT = ChatPromptTemplate.from_template(f.read())

with open('prompts/choose_tool.txt') as f:
    CHOOSE_TOOL_PROMPT_TEMPLATE = f.read()

with open('prompts/summarize_step.txt') as f:
    SUMMARIZE_STEP_PROMPT_TEMPLATE = ChatPromptTemplate.from_template(f.read())

with open('prompts/improve_code.txt') as f:
    IMPROVE_CODE_PROMPT_TEMPLATE = f.read()

class Sibyl:
    def __init__(self):
        cache = SQLiteCache("llm_cache.sqlite")
        self.llm = ChatOpenAI(model=MODEL, temperature=0, streaming=False, max_retries=5, api_key=OPENAI_API_KEY, base_url=OPENAI_API_BASE, cache=cache)
        self.llm_without_cache = ChatOpenAI(model=MODEL, temperature=0.1, streaming=False, max_retries=5, api_key=OPENAI_API_KEY, base_url=OPENAI_API_BASE)
        self.format_answer_chain = FORMAT_ANSWER_PROMPT | self.llm | StrOutputParser()

        self.tool_choice_output_parser = JsonOutputParser(pydantic_object=ToolChoice)
        choose_tool_prompt = PromptTemplate(
            template=CHOOSE_TOOL_PROMPT_TEMPLATE, 
            input_variables=['steps', 'question'], 
            partial_variables={"format_instructions": self.tool_choice_output_parser.get_format_instructions()}
        )
        self.choose_tool_chain = choose_tool_prompt | self.llm | self.tool_choice_output_parser
        self.choose_tool_chain_without_cache = choose_tool_prompt | self.llm_without_cache | self.tool_choice_output_parser

        self.improve_code_output_parser = JsonOutputParser(pydantic_object=ImproveCode)
        improve_code_prompt = PromptTemplate(
            template=IMPROVE_CODE_PROMPT_TEMPLATE, 
            input_variables=['steps', 'question', 'code'],
            partial_variables={"format_instructions": self.improve_code_output_parser.get_format_instructions()}
        )
        self.improve_code_chain = improve_code_prompt | self.llm | self.improve_code_output_parser
        self.improve_code_chain_without_cache = improve_code_prompt | self.llm_without_cache | self.improve_code_output_parser

        self.summarize_tool_chain = SUMMARIZE_STEP_PROMPT_TEMPLATE | self.llm | StrOutputParser()

        browser_config = {
            "bing_api_key": BING_API_KEY,
            "viewport_size": 1024 * 16,
            "downloads_folder": "coding",
            "request_kwargs": {
                "headers": {"User-Agent": "Mozilla/5.0"}
            },
        }
        self.browser = SimpleTextBrowser(**browser_config)
        self.llm_callback_handler = LLMCallbackHandler()

