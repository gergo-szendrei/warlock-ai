from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.document_ingestion import document_ingestion_api
from app.document_qa import document_qa_api
from app.general_qa import general_qa_api
from app.health import health_api

application = FastAPI()

application.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

application.include_router(document_ingestion_api.router)
application.include_router(document_qa_api.router)
application.include_router(general_qa_api.router)
application.include_router(health_api.router)
