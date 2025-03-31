import logging
import os
from typing import List

from langchain_core.messages import HumanMessage, AIMessage

from app.shared.openapi.history_message import HistoryMessage
from app.shared.openapi.response.qa_preprocess_response import QAPreprocessResponse
from app.shared.service.qa_service_external import register_impure_thought_appearance, get_conversation_history
from app.shared.service.qa_service_internal import is_impure_thoughts, convert_to_chat_history


async def qa(
        qa_preprocess_response: QAPreprocessResponse,
        query: str
) -> str | List[HumanMessage | AIMessage]:
    logging.debug(f"Calling qa with qa_preprocess_response: {qa_preprocess_response} and query: {query}")

    # Check for impure thoughts via Internal Service
    impure_thoughts: bool = is_impure_thoughts(
        query=query,
        user_roles=qa_preprocess_response.user_roles
    )
    if impure_thoughts:
        # Register impure thought appearance via External Service
        register_impure_thought_appearance(user_id=qa_preprocess_response.user_id)
        logging.debug(f"Finished qa with result: {os.environ["PASSAGE_CLASSIFICATION_IMPURE_THOUGHTS_RESPONSE"]}")
        return os.environ["PASSAGE_CLASSIFICATION_IMPURE_THOUGHTS_RESPONSE"]

    # Fetch conversation history via External Service
    history_messages: List[HistoryMessage] = get_conversation_history(
        user_id=qa_preprocess_response.user_id
    )

    # Convert conversation history to chat history via Internal Service
    chat_history: List[HumanMessage | AIMessage] = convert_to_chat_history(history_messages=history_messages)

    logging.debug(f"Finished qa with result: {chat_history}")
    return chat_history
