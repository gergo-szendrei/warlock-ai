import asyncio
import logging
import os

from fastapi import APIRouter

from app.document_ingestion.document_ingestion_service_internal import ingest_document_task
from app.shared.openapi.request.document_ingestion_request import DocumentIngestionRequest

router = APIRouter()


@router.post(
    os.environ["API_PATH_PREFIX"] + os.environ["API_PATH_VERSION"] + "document_ingestion"
)
async def document_ingestion(document_ingestion_request: DocumentIngestionRequest) -> None:
    logging.debug(f"Calling document_ingestion with document_ingestion_request: {document_ingestion_request}")

    # Ingest document via Internal Service
    asyncio.create_task(ingest_document_task(document_ingestion_request))

    logging.debug(f"Finished document_ingestion")
    return
