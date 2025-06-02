import json
import logging
import os
import time
from typing import List, Any, Generator

from fastapi.responses import StreamingResponse
from langchain_core.messages import HumanMessage, AIMessage

from app.shared.chain.impure_thoughts_identifier_chain import Classification, identify_impure_thoughts
from app.shared.openapi.enum.message_type import MessageType
from app.shared.openapi.enum.user_role import UserRole
from app.shared.openapi.history_message import HistoryMessage


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


def handle_error(response: str) -> StreamingResponse:
    logging.debug(f"Calling handle_error with response: {response}")
    error_generator: Generator[str, Any, None] = _create_error_generator(response=response)

    logging.debug(f"Finished handle_error with StreamingResponse")
    return StreamingResponse(error_generator, media_type="text/event-stream")


def _create_error_generator(response: str) -> Generator[str, Any, None]:
    logging.debug(f"Calling _create_error_generator with response: {response}")

    if os.environ["STREAM_TARGET"] == "TERMINAL":
        for token in response.split(" "):
            yield token + " "
            time.sleep(float(os.environ["AGENT_COMMON_RESPONSE_TOKEN_DELAY_SECONDS"]))
    else:
        for token in response.split(" "):
            yield f"data: {json.dumps({'text': token + " "})}\n\n"
            time.sleep(float(os.environ["AGENT_COMMON_RESPONSE_TOKEN_DELAY_SECONDS"]))

    logging.debug(f"Finished _create_error_generator")
