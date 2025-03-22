import logging

import httpx

from app.shared.openapi.response.document_ingestion_response import DocumentIngestionResponse


async def ingest_document_callback(
        document_ingestion_response: DocumentIngestionResponse,
        client: httpx.AsyncClient
) -> None:
    logging.debug(
        f"Calling ingest_document_callback with document_ingestion_response: {document_ingestion_response} and client")

    # TODO - Add CALLBACK URL with External
    # TODO - Handle error path
    # callback_url = f"{os.environ["API_PATH_PREFIX"] + os.environ["API_PATH_VERSION"]}document_ingestion/callback"
    # await client.post(callback_url, json=document_ingestion_response.model_dump())

    logging.debug(f"Finished ingest_document_callback")
