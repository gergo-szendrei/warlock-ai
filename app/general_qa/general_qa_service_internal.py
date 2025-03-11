import asyncio
import logging
import os
import time
from asyncio import Task
from typing import List, AsyncGenerator, Any, Generator

from fastapi.responses import StreamingResponse
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage

from app.general_qa.agent.coding_agent import invoke_coding_agent
from app.general_qa.agent.search_agent import invoke_search_agent
from app.general_qa.agent.stack_agent import invoke_stack_agent
from app.shared.chain.impure_thoughts_identifier import Classification, identify_impure_thoughts
from app.shared.chain.query_category_identifier import identify_query_category
from app.shared.enum.general_qa_query_category import GeneralQAQueryCategory
from app.shared.openapi.enum.message_type import MessageType
from app.shared.openapi.enum.user_role import UserRole
from app.shared.openapi.history_message import HistoryMessage
from app.shared.util.async_callback_handler import AsyncCallbackHandler

agent_map = {
    GeneralQAQueryCategory.CODING: invoke_coding_agent,
    GeneralQAQueryCategory.STACK: invoke_stack_agent,
    GeneralQAQueryCategory.OTHER: invoke_search_agent
}


def is_impure_thoughts(
        query: str,
        user_roles: List[UserRole]
) -> bool:
    logging.debug(f"Calling is_impure_thoughts with query: {query} and user_roles: {user_roles}")
    result: bool = False

    if UserRole.FAVORITE not in user_roles:
        classification: Classification = identify_impure_thoughts(query=query)
        if classification.politics == 1 or classification.terrorism == 1 or classification.pornography == 1:
            result = True

    logging.debug(f"Finished is_impure_thoughts with result: {result}")
    return result


def convert_to_chat_history(history_messages: List[HistoryMessage]) -> List[HumanMessage | AIMessage]:
    logging.debug(f"Calling convert_to_chat_history with history_messages: {history_messages}")
    chat_history: List[HumanMessage | AIMessage] = []

    for history_message in history_messages:
        if history_message.message_type == MessageType.HUMAN:
            chat_history.append(HumanMessage(history_message.message_content))
        else:
            chat_history.append(AIMessage(history_message.message_content))

    logging.debug(f"Finished convert_to_chat_history with chat_history: {chat_history}")
    return chat_history


def get_query_category(query: str) -> GeneralQAQueryCategory:
    logging.debug(f"Calling get_query_category with query: {query}")
    result: BaseMessage = identify_query_category(query=query)

    logging.debug(f"Finished get_query_category with result: {result}")
    return GeneralQAQueryCategory(result.content)


def handle_error(response: str) -> StreamingResponse:
    logging.debug(f"Calling handle_error with response: {response}")
    error_generator: Generator[str, Any, None] = create_error_generator(response=response)

    logging.debug(f"Finished handle_error with StreamingResponse")
    return StreamingResponse(error_generator, media_type="text/event-stream")


def create_error_generator(response: str) -> Generator[str, Any, None]:
    logging.debug(f"Calling create_error_generator with response: {response}")

    for token in response.split(" "):
        yield token + " "
        time.sleep(float(os.environ["AGENT_COMMON_RESPONSE_TOKEN_DELAY_SECONDS"]))

    logging.debug(f"Finished create_error_generator")


def handle_success(
        query: str,
        chat_history: List[HumanMessage | AIMessage],
        query_category: GeneralQAQueryCategory
) -> StreamingResponse:
    logging.debug(f"Calling handle_success with query: {query} and chat_history: {chat_history}")
    iterator: AsyncCallbackHandler = AsyncCallbackHandler()
    success_generator: AsyncGenerator[str, Any] = create_success_generator(
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


async def create_success_generator(
        query: str,
        chat_history: List[HumanMessage | AIMessage],
        query_category: GeneralQAQueryCategory,
        iterator: AsyncCallbackHandler
) -> AsyncGenerator[str, Any]:
    logging.debug(f"Calling create_success_generator with query: {query}, chat_history: {chat_history} and iterator")

    invoke_agent = agent_map.get(query_category)
    task: Task = asyncio.create_task(
        invoke_agent(
            query=query,
            chat_history=chat_history,
            iterator=iterator
        )
    )
    async for token in iterator.aiter():
        yield token
    await task

    logging.debug(f"Finished create_success_generator")
