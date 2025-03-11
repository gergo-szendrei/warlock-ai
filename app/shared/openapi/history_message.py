from pydantic import BaseModel, Field

from app.shared.openapi.enum.message_type import MessageType


class HistoryMessage(BaseModel):
    message_content: str = Field(
        description="""
        Describes the content of a historical message
        """
    )

    message_type: MessageType = Field(
        description="""
        Describes the type of a historical message
        """
    )
