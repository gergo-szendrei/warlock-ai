from typing import List

from pydantic import BaseModel, Field

from app.shared.openapi.enum.user_role import UserRole


class QAPreprocessResponse(BaseModel):
    user_id: str = Field(
        description="""
        Describes the id of a user
        """
    )

    user_roles: List[UserRole] = Field(
        description="""
        Describes the roles of a user
        """
    )
