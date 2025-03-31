import logging
import os
from typing import List

from langchain_core.messages import HumanMessage, AIMessage
from langchain_ollama import ChatOllama

from app.document_qa.prompt.chat_history_using_rag_chain_prompt import chat_history_using_rag_chain_prompt
from app.shared.util.async_callback_handler import AsyncCallbackHandler


async def invoke_retriever_chain(
        query: str,
        context: str,
        chat_history: List[HumanMessage | AIMessage],
        iterator: AsyncCallbackHandler
):
    logging.debug(f"""
        Calling invoke_retriever_chain with query: {query}, context: {context}, 
        chat_history: {chat_history} and iterator
    """)

    model = ChatOllama(
        model=os.environ["LLM_MODEL"],
        base_url=os.environ["LLM_BASE_URL"],
        temperature=float(os.environ["LLM_TEMPERATURE"]),
        callbacks=[iterator],
        disable_streaming=False
    )

    base_prompt = chat_history_using_rag_chain_prompt
    prompt = base_prompt.partial(
        query=query,
        context=context,
        chat_history=chat_history
    )

    chain = prompt | model

    logging.debug(f"Finished invoke_retriever_chain, starting stream")
    await chain.ainvoke(
        input={
            "query": query,
            "context": context,
            "chat_history": chat_history
        }
    )
