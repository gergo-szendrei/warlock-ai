import os
from typing import List

from langchain import hub
from langchain.agents import (
    create_react_agent,
    AgentExecutor
)
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_core.messages import HumanMessage, AIMessage
from langchain_ollama import ChatOllama

from app.shared.util.async_callback_handler import AsyncCallbackHandler


async def invoke_search_agent(
        query: str,
        chat_history: List[HumanMessage | AIMessage],
        iterator: AsyncCallbackHandler) -> None:
    model = ChatOllama(
        model=os.environ["LLM_MODEL"],
        temperature=float(os.environ["LLM_TEMPERATURE"]),
        callbacks=[iterator],
        disable_streaming=False
    )

    instructions = """
        You are an agent designed to utilize internet search engines to answer questions.
        You have access to the capabilities of DuckDuckGo search.
        Use the result of the search to answer the question.
        If it does not seem like you can answer the question, just return "I don't know" as the answer.
    """

    tools = [DuckDuckGoSearchResults()]
    tool_names = ["duckduckgo_results_json"]

    base_prompt = hub.pull(os.environ["LLM_REACT_PROMPT"])
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

    await agent_executor.ainvoke(
        input={
            "input": query,
            "chat_history": chat_history
        }
    )
