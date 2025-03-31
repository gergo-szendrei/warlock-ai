import logging
import os
from typing import List

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from langchain_core.messages import HumanMessage, AIMessage

from app.general_qa.enum.general_qa_query_category import GeneralQAQueryCategory
from app.general_qa.general_qa_service_external import preprocess_general_qa_request
from app.general_qa.general_qa_service_internal import handle_success, get_query_category
from app.shared.api.qa_api import qa
from app.shared.openapi.request.general_qa_request import GeneralQARequest
from app.shared.openapi.response.qa_preprocess_response import QAPreprocessResponse
from app.shared.service.qa_service_internal import handle_error

router = APIRouter()


@router.post(
    os.environ["API_PATH_PREFIX"] + os.environ["API_PATH_VERSION"] + "general_qa",
    response_model=None
)
async def general_qa(general_qa_request: GeneralQARequest) -> StreamingResponse | str:
    logging.debug(f"Calling general_qa with general_qa_request: {general_qa_request}")

    # Preprocess via External Service
    qa_preprocess_response: QAPreprocessResponse = preprocess_general_qa_request(
        warlock_api_key=general_qa_request.warlock_api_key
    )

    # Run shared QA logic
    shared_qa_result: str | List[HumanMessage | AIMessage] = await qa(
        qa_preprocess_response=qa_preprocess_response,
        query=general_qa_request.query
    )

    # Impure thoughts path
    if type(shared_qa_result) is str:
        # Respond error via Internal Service
        return handle_error(shared_qa_result)

    # Identify query category via Internal Service
    query_category: GeneralQAQueryCategory = get_query_category(query=general_qa_request.query)

    logging.debug(f"Finished general_qa, starting stream")
    # Respond success via Internal Service
    return handle_success(
        query=general_qa_request.query,
        chat_history=shared_qa_result,
        query_category=query_category
    )
