import logging
import os
from typing import List

import httpx
from fastapi import HTTPException, status
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings
from langchain_postgres import PGVector
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.document_ingestion.document_ingestion_service_external import ingest_document_callback
from app.shared.openapi.enum.document_type import DocumentType
from app.shared.openapi.request.document_ingestion_request import DocumentIngestionRequest
from app.shared.openapi.response.document_ingestion_response import DocumentIngestionResponse


async def ingest_document_task(document_ingestion_request: DocumentIngestionRequest) -> None:
    try:
        async with httpx.AsyncClient() as client:
            logging.debug(
                f"Calling ingest_document_task with document_ingestion_request: {document_ingestion_request}")

            await ingest_document(document_ingestion_request)

            document_ingestion_response = DocumentIngestionResponse.model_validate({
                "document_id": document_ingestion_request.document_id
            })
            await ingest_document_callback(document_ingestion_response, client)

            logging.debug(f"Finished ingest_document_task")
    except Exception as e:
        message = f"An error occurred during ingest_document_task: {e}"
        logging.exception(message)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=message
        ) from e


async def ingest_document(document_ingestion_request: DocumentIngestionRequest) -> None:
    logging.debug(f"Calling ingest_document with document_ingestion_request: {document_ingestion_request}")

    loader: PyPDFLoader | WebBaseLoader = get_loader(
        document_ingestion_request.document_type,
        document_ingestion_request.document_path
    )
    document: List[Document] = loader.load()

    text_splitter: RecursiveCharacterTextSplitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    sub_documents: List[Document] = text_splitter.split_documents(document)

    for sub_document in sub_documents:
        sub_document.metadata = {
            "id": document_ingestion_request.document_id,
            "user_id": document_ingestion_request.user_id,
            "subject_id": document_ingestion_request.subject_id,
            "topic_id": document_ingestion_request.topic_id
        }

    vector_store: PGVector = get_vector_store()
    vector_store.add_documents(
        documents=sub_documents,
        ids=[sub_document.metadata["id"] for sub_document in sub_documents]
    )

    logging.debug(f"Finished ingest_document")


def get_loader(
        document_type: DocumentType,
        document_path: str
) -> PyPDFLoader | WebBaseLoader:
    logging.debug(f"Calling get_loader with document_type: {document_type} and document_path: {document_path}")

    if document_type == DocumentType.PDF:
        logging.debug(f"Finished get_loader with PyPDFLoader")
        return PyPDFLoader(document_path)
    else:
        logging.debug(f"Finished get_loader with WebBaseLoader")
        return WebBaseLoader(document_path)


def get_vector_store() -> PGVector:
    logging.debug(f"Calling get_vector_store")

    embeddings: OllamaEmbeddings = OllamaEmbeddings(model=os.environ["LLM_MODEL"])

    connection: str = f"postgresql+psycopg://{os.environ["POSTGRES_USER"]}:{os.environ["POSTGRES_PASSWORD"]}@{os.environ["POSTGRES_HOST"]}:{os.environ["POSTGRES_PORT"]}/{os.environ["POSTGRES_DATABASE"]}"

    collection_name: str = "langchain"

    logging.debug(f"Finished get_vector_store with PGVector")
    return PGVector(
        embeddings=embeddings,
        connection=connection,
        collection_name=collection_name,
        use_jsonb=True
    )
