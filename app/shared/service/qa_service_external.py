import logging
from typing import List

from app.shared.openapi.enum.message_type import MessageType
from app.shared.openapi.history_message import HistoryMessage


def register_impure_thought_appearance(user_id: str) -> None:
    logging.debug(f"Calling register_impure_thought_appearance with user_id: {user_id}")

    # TODO - Implement SYNC API call with External
    # TODO - Handle error path

    logging.debug(f"Finished register_impure_thought_appearance")


def get_conversation_history(user_id: str) -> List[HistoryMessage]:
    logging.debug(f"Calling get_conversation_history with user_id: {user_id}")

    # TODO - Implement SYNC API call with External
    # TODO - Handle error path
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

    logging.debug(f"Finished get_conversation_history with history_messages: {history_messages}")
    return history_messages


def save_new_message_to_history(
        user_id: str,
        subject_id: int,
        topic_id: int,
        message_content: str
) -> None:
    logging.debug(f"""
        Calling save_new_message_to_history with user_id: {user_id}, subject_id: {subject_id},
        topic_id: {topic_id} and message_content: {message_content}
    """)

    # TODO - Implement SYNC API call with External
    # TODO - Handle error path

    logging.debug(f"Finished save_new_message_to_history")
