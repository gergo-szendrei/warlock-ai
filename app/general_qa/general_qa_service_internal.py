import asyncio
import json
import logging
import os
from asyncio import Task
from typing import List, AsyncGenerator, Any

from fastapi.responses import StreamingResponse
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage

from app.general_qa.agent.coding_agent import invoke_coding_agent
from app.general_qa.agent.search_agent import invoke_search_agent
from app.general_qa.agent.stack_agent import invoke_stack_agent
from app.general_qa.chain.query_category_identifier_chain import identify_query_category
from app.general_qa.enum.general_qa_query_category import GeneralQAQueryCategory
from app.shared.util.async_callback_handler import AsyncCallbackHandler

agent_map = {
    GeneralQAQueryCategory.CODING: invoke_coding_agent,
    GeneralQAQueryCategory.STACK: invoke_stack_agent,
    GeneralQAQueryCategory.OTHER: invoke_search_agent
}


def get_query_category(query: str) -> GeneralQAQueryCategory:
    logging.debug(f"Calling get_query_category with query: {query}")
    result: BaseMessage = identify_query_category(query=query)

    logging.debug(f"Finished get_query_category with result: {result.content}")
    return GeneralQAQueryCategory(result.content)


def handle_success(
        query: str,
        chat_history: List[HumanMessage | AIMessage],
        user_id: int,
        query_category: GeneralQAQueryCategory
) -> StreamingResponse:
    logging.debug(f"""
        Calling handle_success with query: {query}, chat_history: {chat_history},
        user_id: {user_id} and query_category: {query_category}
    """)
    iterator: AsyncCallbackHandler = AsyncCallbackHandler(
        query=query,
        user_id=user_id
    )
    success_generator: AsyncGenerator[str, Any] = _create_success_generator(
        query=query,
        chat_history=chat_history,
        query_category=query_category,
        iterator=iterator
    )

    logging.debug(f"Finished handle_success with StreamingResponse")
    return StreamingResponse(
        content=success_generator,
        media_type="text/event-stream"
    )


async def _create_success_generator(
        query: str,
        chat_history: List[HumanMessage | AIMessage],
        query_category: GeneralQAQueryCategory,
        iterator: AsyncCallbackHandler
) -> AsyncGenerator[str, Any]:
    logging.debug(f""" 
        Calling _create_success_generator with query: {query}, 
        chat_history: {chat_history}, query_category: {query_category} and iterator
    """)

    invoke_agent = agent_map.get(query_category)
    task: Task = asyncio.create_task(
        invoke_agent(
            query=query,
            chat_history=chat_history,
            iterator=iterator
        )
    )

    if os.environ["STREAM_TARGET"] == "TERMINAL":
        async for token in iterator.aiter():
            yield token
    else:
        async for token in iterator.aiter():
            yield f"data: {json.dumps({'text': token})}\n\n"
    await task

    logging.debug(f"Finished _create_success_generator")
