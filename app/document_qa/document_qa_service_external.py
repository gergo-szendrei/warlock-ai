import logging
import os

from app.shared.openapi.enum.user_role import UserRole
from app.shared.openapi.response.qa_preprocess_response import QAPreprocessResponse


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
            pass
            # TODO - Implement SYNC API call with External
        else:
            qa_preprocess_response: QAPreprocessResponse = QAPreprocessResponse.model_validate({
                "user_id": "5848988d-255c-48ba-a975-3aa567f1fe3e",
                "user_roles": [UserRole.STUDENT]
            })
    except Exception as e:
        message = f"An error occurred during preprocess_document_qa_request: {e}"
        logging.exception(message)
        raise e

    logging.debug(
        f"Finished preprocess_document_qa_request with qa_preprocess_response: {qa_preprocess_response}")
    return qa_preprocess_response
