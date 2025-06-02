import logging
import os

import requests

from app.shared.openapi.enum.user_role import UserRole
from app.shared.openapi.response.qa_preprocess_response import QAPreprocessResponse
from app.shared.util.external_service_util import backend_common_headers, backend_url_static_part, \
    parse_response_content


def preprocess_general_qa_request(warlock_api_key: str) -> QAPreprocessResponse:
    logging.debug(f"Calling preprocess_general_qa_request with warlock_api_key: {warlock_api_key}")

    try:
        if os.environ["MOCK_BACKEND"] != "True":
            response = requests.post(
                url=backend_url_static_part + "validate-user",
                headers=backend_common_headers,
                json={
                    "token": warlock_api_key
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
        message = f"An error occurred during preprocess_general_qa_request: {e}"
        logging.exception(message)
        raise e

    logging.debug(
        f"Finished preprocess_general_qa_request with qa_preprocess_response: {qa_preprocess_response}")
    return qa_preprocess_response
