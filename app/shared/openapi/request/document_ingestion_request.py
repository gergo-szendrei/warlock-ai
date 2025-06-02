from pydantic import BaseModel, Field

from app.shared.openapi.enum.document_type import DocumentType


class DocumentIngestionRequest(BaseModel):
    user_id: int = Field(
        description="""
            Describes the id of a user
            """
    )

    subject_id: int = Field(
        description="""
            Describes the id of a subject
            """
    )

    topic_id: int = Field(
        description="""
            Describes the id of a topic
            """
    )

    document_path: str = Field(
        description="""
            Describes the complete path of the document on the file server,
            Format follows: main_directory/sub_directory/.../name.extension
            """
    )

    document_id: int = Field(
        description="""
            Describes the id of a document
            """
    )

    document_type: DocumentType = Field(
        description="""
            Describes the type of a document
            """
    )
