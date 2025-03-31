from pydantic import BaseModel, Field


class DocumentQARequest(BaseModel):
    query: str = Field(
        description="""
        Describes the UI chat input of a user
        """
    )

    warlock_api_key: str = Field(
        description="""
        Describes the unique api key of a user
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
