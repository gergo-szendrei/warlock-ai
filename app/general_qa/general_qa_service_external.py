import logging
from typing import List

from app.shared.openapi.enum.message_type import MessageType
from app.shared.openapi.enum.user_role import UserRole
from app.shared.openapi.history_message import HistoryMessage
from app.shared.openapi.response.general_qa_preprocess_response import GeneralQAPreprocessResponse


def preprocess_general_qa_request(warlock_api_key: str) -> GeneralQAPreprocessResponse:
    logging.debug(f"Calling preprocess_general_qa_request with warlock_api_key: {warlock_api_key}")

    # TODO - Implement SYNC API call with External
    # TODO - Handle error path
    general_qa_preprocess_response: GeneralQAPreprocessResponse = GeneralQAPreprocessResponse.model_validate({
        "user_id": "5848988d-255c-48ba-a975-3aa567f1fe3e",
        "user_roles": [UserRole.STUDENT]
    })

    logging.debug(
        f"Finished preprocess_general_qa_request with general_qa_preprocess_response: {general_qa_preprocess_response}")
    return general_qa_preprocess_response


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
