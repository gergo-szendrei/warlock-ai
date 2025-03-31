import logging
import os
from typing import List

from langchain.agents import (
    create_react_agent,
    AgentExecutor
)
from langchain_core.messages import HumanMessage, AIMessage
from langchain_experimental.tools import PythonREPLTool
from langchain_ollama import ChatOllama

from app.general_qa.prompt.tool_forced_react_agent_prompt import tool_forced_react_agent_prompt
from app.shared.util.async_callback_handler import AsyncCallbackHandler


async def invoke_coding_agent(
        query: str,
        chat_history: List[HumanMessage | AIMessage],
        iterator: AsyncCallbackHandler) -> None:
    logging.debug(f"Calling invoke_coding_agent with query: {query}, chat_history: {chat_history} and iterator")

    model = ChatOllama(
        model=os.environ["LLM_MODEL"],
        base_url=os.environ["LLM_BASE_URL"],
        temperature=float(os.environ["LLM_TEMPERATURE"]),
        callbacks=[iterator],
        disable_streaming=False
    )

    instructions = """
        You are an agent designed to write and execute python (with or without numpy) to answer 
        mathematical, statistical and probability questions.
        You have access to a Python 3.12 and numpy.
        To use numpy you have to run 'import numpy as np' and reference it as 'np' afterwards.
        If you get an error, debug your code and try again.
        Only use the output of your code to answer the question. 
        You might know the answer without running any code, but you should still run the code to get the answer.
        If it does not seem like you can write code to answer the question, just return "I don't know" as the answer.
    """

    tools = [PythonREPLTool()]
    tool_names = ["Python_REPL"]

    base_prompt = tool_forced_react_agent_prompt
    prompt = base_prompt.partial(
        instructions=instructions,
        tools=tools,
        tool_names=tool_names
    )

    agent = create_react_agent(
        llm=model,
        tools=tools,
        prompt=prompt
    )

    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=os.environ["AGENT_COMMON_VERBOSE_LOGGING"] == "True"
    )

    logging.debug(f"Finished invoke_coding_agent, starting stream")
    await agent_executor.ainvoke(
        input={
            "input": query,
            "chat_history": chat_history
        }
    )
