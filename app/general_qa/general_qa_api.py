import logging
import os
from typing import List

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from langchain_core.messages import HumanMessage, AIMessage

from app.general_qa.general_qa_service_external import preprocess_general_qa_request, get_conversation_history, \
    register_impure_thought_appearance
from app.general_qa.general_qa_service_internal import is_impure_thoughts, convert_to_chat_history, handle_error, \
    handle_success, get_query_category
from app.shared.enum.general_qa_query_category import GeneralQAQueryCategory
from app.shared.openapi.history_message import HistoryMessage
from app.shared.openapi.request.general_qa_request import GeneralQARequest
from app.shared.openapi.response.general_qa_preprocess_response import GeneralQAPreprocessResponse

router = APIRouter()


@router.post(
    os.environ["API_PATH_PREFIX"] + os.environ["API_PATH_VERSION"] + "general_qa",
    response_model=None
)
async def general_qa(general_qa_request: GeneralQARequest) -> StreamingResponse | str:
    logging.debug(f"Calling general_qa with general_qa_request: {general_qa_request}")

    # Preprocess via External Service
    general_qa_preprocess_response: GeneralQAPreprocessResponse = preprocess_general_qa_request(
        warlock_api_key=general_qa_request.warlock_api_key
    )

    # Check for impure thoughts via Internal Service
    impure_thoughts: bool = is_impure_thoughts(
        query=general_qa_request.query,
        user_roles=general_qa_preprocess_response.user_roles
    )
    if impure_thoughts:
        # Register impure thought appearance via External Service
        register_impure_thought_appearance(user_id=general_qa_preprocess_response.user_id)
        # Respond via Internal Service
        return handle_error(os.environ["PASSAGE_CLASSIFICATION_IMPURE_THOUGHTS_RESPONSE"])

    # Fetch conversation history via External Service
    history_messages: List[HistoryMessage] = get_conversation_history(
        user_id=general_qa_preprocess_response.user_id
    )

    # Convert conversation history to chat history via Internal Service
    chat_history: List[HumanMessage | AIMessage] = convert_to_chat_history(history_messages=history_messages)

    # Identify query category via Internal Service
    query_category: GeneralQAQueryCategory = get_query_category(query=general_qa_request.query)

    logging.debug(f"Finished general_qa, starting stream")
    # Respond via Internal Service
    return handle_success(
        query=general_qa_request.query,
        chat_history=chat_history,
        query_category=query_category
    )
