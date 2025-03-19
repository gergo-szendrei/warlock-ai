import os

from fastapi import APIRouter

router = APIRouter()


@router.get(
    os.environ["API_PATH_PREFIX"] + os.environ["API_PATH_VERSION"] + "health"
)
def health() -> str:
    return "Alive"
