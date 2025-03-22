from pydantic import BaseModel, Field


class DocumentIngestionResponse(BaseModel):
    document_id: int = Field(
        description="""
            Describes the id of a document
            """
    )
