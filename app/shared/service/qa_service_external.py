import logging
import os
from typing import List

import requests

from app.shared.openapi.enum.message_type import MessageType
from app.shared.openapi.history_message import HistoryMessage
from app.shared.util.external_service_util import backend_common_headers, backend_url_static_part, \
    parse_response_content


def register_impure_thought_appearance(user_id: int) -> None:
    logging.debug(f"Calling register_impure_thought_appearance with user_id: {user_id}")

    try:
        if os.environ["MOCK_BACKEND"] != "True":
            requests.put(
                url=backend_url_static_part + "add-strike-to-user",
                headers=backend_common_headers,
                json={
                    "user_id": user_id
                }
            )
    except Exception as e:
        message = f"An error occurred during register_impure_thought_appearance: {e}"
        logging.exception(message)
        raise e

    logging.debug(f"Finished register_impure_thought_appearance")


def get_conversation_history(user_id: int) -> List[HistoryMessage]:
    logging.debug(f"Calling get_conversation_history with user_id: {user_id}")

    try:
        if os.environ["MOCK_BACKEND"] != "True":
            response = requests.get(
                url=backend_url_static_part + "get-conversation-history",
                headers=backend_common_headers,
                params={
                    "user_id": user_id
                }
            )
            history_messages: List[HistoryMessage] = [
                HistoryMessage.model_validate(el) for el in parse_response_content(response.content)
            ]
        else:
            history_messages: List[HistoryMessage] = [
                HistoryMessage.model_validate({
                    "message_content": "Hi! My name is George.",
                    "message_type": MessageType.HUMAN
                }),
                HistoryMessage.model_validate({
                    "message_content": "Hi George, it's nice to meet you too! You've mentioned your name earlier. "
                                       + "How can I assist you today?",
                    "message_type": MessageType.AI
                })
            ]
    except Exception as e:
        message = f"An error occurred during get_conversation_history: {e}"
        logging.exception(message)
        raise e

    logging.debug(f"Finished get_conversation_history with history_messages: {history_messages}")
    return history_messages


def save_new_message_to_history(
        user_id: int,
        subject_id: int,
        topic_id: int,
        human_message_content: str,
        ai_message_content: str
) -> None:
    logging.debug(f"""
        Calling save_new_message_to_history with user_id: {user_id}, subject_id: {subject_id}, topic_id: {topic_id}, 
        human_message_content: {human_message_content} and ai_message_content: {ai_message_content}
    """)

    try:
        if os.environ["MOCK_BACKEND"] != "True":
            requests.post(
                url=backend_url_static_part + "save-qa",
                headers=backend_common_headers,
                json={
                    "user_id": user_id,
                    "subject_id": subject_id,
                    "topic_id": topic_id,
                    "human_message_content": human_message_content,
                    "ai_message_content": ai_message_content
                }
            )
    except Exception as e:
        message = f"An error occurred during save_new_message_to_history: {e}"
        logging.exception(message)
        raise e

    logging.debug(f"Finished save_new_message_to_history")
