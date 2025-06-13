import logging
import os
from typing import List

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from langchain_core.messages import HumanMessage, AIMessage

from app.document_qa.document_qa_service_external import preprocess_document_qa_request
from app.document_qa.document_qa_service_internal import handle_success, get_context
from app.shared.api.qa_api import qa
from app.shared.openapi.request.document_qa_request import DocumentQARequest
from app.shared.openapi.response.qa_preprocess_response import QAPreprocessResponse
from app.shared.service.qa_service_internal import handle_error

router = APIRouter()


@router.post(
    os.environ["API_PATH_PREFIX"] + os.environ["API_PATH_VERSION"] + "document-qa",
    response_model=None
)
async def document_qa(document_qa_request: DocumentQARequest) -> StreamingResponse | str:
    try:
        logging.debug(f"Calling document_qa with document_qa_request: {document_qa_request}")

        # Preprocess via External Service
        qa_preprocess_response: QAPreprocessResponse = preprocess_document_qa_request(
            warlock_api_key=document_qa_request.warlock_api_key,
            topic_id=document_qa_request.topic_id,
            subject_id=document_qa_request.subject_id
        )

        # Run shared QA logic
        shared_qa_result: str | List[HumanMessage | AIMessage] = await qa(
            qa_preprocess_response=qa_preprocess_response,
            query=document_qa_request.query
        )

        # Impure thoughts path
        if type(shared_qa_result) is str:
            # Respond error via Internal Service
            return handle_error(shared_qa_result)

        # Get context from vector store via Internal Service
        context = get_context(
            query=document_qa_request.query,
            user_id=qa_preprocess_response.user_id,
            subject_id=document_qa_request.subject_id,
            topic_id=document_qa_request.topic_id
        )

        logging.debug(f"Finished document_qa, starting stream")
        # Respond success via Internal Service
        return handle_success(
            query=document_qa_request.query,
            context=context,
            user_id=qa_preprocess_response.user_id,
            subject_id=document_qa_request.subject_id,
            topic_id=document_qa_request.topic_id,
            chat_history=shared_qa_result
        )
    except Exception as e:
        message = f"An error occurred during document_qa: {e}"
        logging.exception(message)
        return handle_error(message)
