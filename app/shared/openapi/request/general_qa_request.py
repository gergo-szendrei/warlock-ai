from pydantic import BaseModel, Field


class GeneralQARequest(BaseModel):
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
