import logging
import os
from typing import List

from langchain.agents import (
    AgentExecutor,
    create_react_agent
)
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain_core.messages import HumanMessage, AIMessage
from langchain_ollama import ChatOllama

from app.general_qa.prompt.tool_forced_no_thought_react_agent_prompt import tool_forced_no_thought_react_agent_prompt
from app.shared.util.async_callback_handler import AsyncCallbackHandler


async def invoke_stack_agent(
        query: str,
        chat_history: List[HumanMessage | AIMessage],
        iterator: AsyncCallbackHandler) -> None:
    logging.debug(f"Calling invoke_stack_agent with query: {query}, chat_history: {chat_history} and iterator")

    model = ChatOllama(
        model=os.environ["LLM_MODEL"],
        base_url=os.environ["LLM_BASE_URL"],
        temperature=float(os.environ["LLM_TEMPERATURE"]),
        callbacks=[iterator],
        disable_streaming=False
    )

    instructions = """
        You are an agent designed to provide fixes for bugs, issues, errors, problems or anomalies related to coding.
        You have access to StackOverFlow.
        Use the result of the search to answer the question.
        If it does not seem like you can answer the question, just return "I don't know" as the answer.
    """

    tools = load_tools(["stackexchange"])
    tool_names = ["stackexchange"]

    base_prompt = tool_forced_no_thought_react_agent_prompt
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

    logging.debug(f"Finished invoke_stack_agent, starting stream")
    await agent_executor.ainvoke(
        input={
            "input": query,
            "chat_history": chat_history
        }
    )
