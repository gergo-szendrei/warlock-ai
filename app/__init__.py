from fastapi import FastAPI

from app.general_qa import general_qa_api

application = FastAPI()

application.include_router(general_qa_api.router)
