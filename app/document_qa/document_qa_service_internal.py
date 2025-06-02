import asyncio
import json
import logging
import os
from asyncio import Task
from typing import List, AsyncGenerator, Any

from fastapi.responses import StreamingResponse
from langchain_core.messages import HumanMessage, AIMessage

from app.document_qa.chain.retriever_chain import invoke_retriever_chain
from app.shared.service.document_service_internal import get_vector_store
from app.shared.util.async_callback_handler import AsyncCallbackHandler


def get_context(
        query: str,
        user_id: str,
        subject_id: int,
        topic_id: int
) -> str:
    logging.debug(f""" 
        Calling get_context with query: {query}, user_id: {user_id},
        subject_id: {subject_id} and topic_id: {topic_id}
    """)
    vector_store = get_vector_store()
    retrieved_docs = vector_store.similarity_search(
        query=query,
        k=3,
        filter={
            "$and": [
                {"user_id": {"$eq": user_id}},
                {"subject_id": {"$eq": subject_id}},
                {"topic_id": {"$eq": topic_id}}
            ]
        }
    )
    context = "\n\n".join(retrieved_doc.page_content for retrieved_doc in retrieved_docs)

    logging.debug(f"Finished get_context with context: {context}")
    return context


def handle_success(
        query: str,
        context: str,
        user_id: str,
        subject_id: int,
        topic_id: int,
        chat_history: List[HumanMessage | AIMessage]
) -> StreamingResponse:
    logging.debug(f""" 
        Calling handle_success with query: {query}, context: {context}, user_id: {user_id},
        subject_id: {subject_id}, topic_id: {topic_id} and chat_history: {chat_history}
    """)
    iterator: AsyncCallbackHandler = AsyncCallbackHandler(
        user_id=user_id,
        subject_id=subject_id,
        topic_id=topic_id
    )
    success_generator: AsyncGenerator[str, Any] = _create_success_generator(
        query=query,
        context=context,
        chat_history=chat_history,
        iterator=iterator
    )

    logging.debug(f"Finished handle_success with StreamingResponse")
    return StreamingResponse(
        content=success_generator,
        media_type="text/event-stream"
    )


async def _create_success_generator(
        query: str,
        context: str,
        chat_history: List[HumanMessage | AIMessage],
        iterator: AsyncCallbackHandler
) -> AsyncGenerator[str, Any]:
    logging.debug(f"""
        Calling _create_success_generator with query: {query}, context: {context},
        chat_history: {chat_history} and iterator
    """)

    task: Task = asyncio.create_task(
        invoke_retriever_chain(
            query=query,
            context=context,
            chat_history=chat_history,
            iterator=iterator
        )
    )

    if os.environ["STREAM_TARGET"] == "TERMINAL":
        async for token in iterator.aiter():
            yield token
    else:
        async for token in iterator.aiter():
            yield f"data: {json.dumps({'text': token})}\n\n"
    await task

    logging.debug(f"Finished _create_success_generator")
