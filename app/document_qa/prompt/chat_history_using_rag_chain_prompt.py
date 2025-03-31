from langchain_core.prompts import PromptTemplate

chat_history_using_rag_chain_template = """
    You are an assistant for query-answering tasks. 
    Use the following pieces of retrieved context and chat history to answer the query. 
    If you don't know the answer, just say that you don't know. 
    Use three sentences maximum and keep the answer concise.
    
    Query: {query}
    Context: {context}
    Chat history: {chat_history}
    
    You MUST respond to the human, and you MUST use the format:
    
    ```
    Final Answer: [your response here]
    ```
"""

chat_history_using_rag_chain_prompt = PromptTemplate(
    template=chat_history_using_rag_chain_template,
    input_variables=[
        "query",
        "context",
        "chat_history"
    ]
)
