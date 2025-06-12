import logging
import os

import requests

from app.shared.openapi.enum.user_role import UserRole
from app.shared.openapi.response.qa_preprocess_response import QAPreprocessResponse
from app.shared.util.external_service_util import backend_url_static_part, backend_common_headers, \
    parse_response_content


def preprocess_document_qa_request(
        warlock_api_key: str,
        topic_id: int,
        subject_id: int
) -> QAPreprocessResponse:
    logging.debug(f"""
        Calling preprocess_document_qa_request with warlock_api_key: {warlock_api_key}, 
        topic_id: {topic_id} and subject_id: {subject_id}
    """)

    try:
        if os.environ["MOCK_BACKEND"] != "True":
            response = requests.post(
                url=backend_url_static_part + "validate-user-document-qa",
                headers=backend_common_headers,
                json={
                    "warlock_api_key": warlock_api_key,
                    "topic_id": topic_id,
                    "subject_id": subject_id
                }
            )
            qa_preprocess_response: QAPreprocessResponse = QAPreprocessResponse.model_validate({
                **parse_response_content(response.content)
            })
        else:
            qa_preprocess_response: QAPreprocessResponse = QAPreprocessResponse.model_validate({
                "user_id": 111,
                "user_roles": [UserRole.STUDENT]
            })
    except Exception as e:
        message = f"An error occurred during preprocess_document_qa_request: {e}"
        logging.exception(message)
        raise e

    logging.debug(
        f"Finished preprocess_document_qa_request with qa_preprocess_response: {qa_preprocess_response}")
    return qa_preprocess_response
