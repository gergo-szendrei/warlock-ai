import logging
import os

from langchain_ollama import OllamaEmbeddings
from langchain_postgres import PGVector


def get_vector_store() -> PGVector:
    logging.debug(f"Calling get_vector_store")

    embeddings: OllamaEmbeddings = OllamaEmbeddings(model=os.environ["LLM_MODEL"])

    user_info: str = f"{os.environ["POSTGRES_USER"]}:{os.environ["POSTGRES_PASSWORD"]}"
    db_info: str = f"{os.environ["POSTGRES_HOST"]}:{os.environ["POSTGRES_PORT"]}/{os.environ["POSTGRES_DATABASE"]}"
    connection: str = f"postgresql+psycopg://{user_info}@{db_info}"

    collection_name: str = "langchain"

    logging.debug(f"Finished get_vector_store with PGVector")
    return PGVector(
        embeddings=embeddings,
        connection=connection,
        collection_name=collection_name,
        use_jsonb=True
    )
