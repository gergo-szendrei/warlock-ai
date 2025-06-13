import logging
import os

import httpx

from app.shared.openapi.response.document_ingestion_response import DocumentIngestionResponse
from app.shared.util.external_service_util import backend_url_static_part


async def ingest_document_callback(
        document_ingestion_response: DocumentIngestionResponse,
        client: httpx.AsyncClient
) -> None:
    logging.debug(
        f"Calling ingest_document_callback with document_ingestion_response: {document_ingestion_response} and client")

    try:
        if os.environ["MOCK_BACKEND"] != "True":
            pass
            callback_url = backend_url_static_part + "document-ingestion-callback"
            await client.post(callback_url, json=document_ingestion_response.model_dump())
    except Exception as e:
        message = f"An error occurred during ingest_document_callback: {e}"
        logging.exception(message)
        raise e

    logging.debug(f"Finished ingest_document_callback")
