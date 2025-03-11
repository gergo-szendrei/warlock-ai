import logging
import os

from langchain_core.messages import BaseMessage
from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate
from langchain_ollama import ChatOllama

model = ChatOllama(
    model=os.environ["LLM_MODEL"],
    temperature=float(os.environ["LLM_TEMPERATURE"])
)

prefix_template = """         
    --- Context START ---
    You are a helpful tool designed to categorize the queries of university student.
    Determine the category of each query based on its content.
    --- Context END ---

    --- Instructions START ---
    If the query requires python code execution, practical numpy usage or the output of executed python code, 
    then it is CAT_1 category.    
    
    If the query cannot be put in CAT_1 category, and relates to either coding bugs, coding errors or coding stacktrace, 
    then it is CAT_2 category.

    If the query cannot be out in neither CAT_1 category, not CAT_2 category,
    then it is CAT_0 category.
        
    ONLY RETURN THE IDENTIFIED CATEGORY.
    --- Instructions END ---
    
    --- Examples START ---
"""

examples = [
    {
        "query": "What is the mean square error, where n = 3, predictions = [1, 1, 1] and labels = [1, 2, 3]?",
        "answer": "CAT_1"
    },
    {
        "query": """
            What dimensions will the new array have, if you call reshape(3, 2) 
            on an array of [0, 1, 2, 3, 4, 5]?
        """,
        "answer": "CAT_1"
    },
    {
        "query": "What will you get if you print 3 + '2' in python?",
        "answer": "CAT_1"
    },
    {
        "query": "How to resolve error 'zsh: redirection with no command'?",
        "answer": "CAT_2"
    },
    {
        "query": "Why do I get the bug 'TypeError: can only concatenate str (not int) to str'?",
        "answer": "CAT_2"
    },
    {
        "query": """
            Explain this stacktrace message: 'Input should be a valid integer, 
            unable to parse string as an integer [type=int_parsing, input_value='bad', input_type=str]'!
        """,
        "answer": "CAT_2"
    },
    {
        "query": "Who was the winner in Formula 1 in 2024?",
        "answer": "CAT_0"
    },
    {
        "query": "How am I called?",
        "answer": "CAT_0"
    },
    {
        "query": "What is the weather like in Kyoto today?",
        "answer": "CAT_0"
    }
]

example_template = """
    query: {query}
    answer: {answer}
"""

example_prompt = PromptTemplate(
    template=example_template,
    input_variables=["query", "answer"]
)

suffix_template = """
    --- Examples END ---
    
    BEGIN!
    
    User query:
    {query}
"""

prompt = FewShotPromptTemplate(
    prefix=prefix_template,
    examples=examples,
    example_prompt=example_prompt,
    suffix=suffix_template,
    input_variables=["query"]
)

chain = prompt | model


def identify_query_category(query: str) -> BaseMessage:
    logging.debug(f"Calling identify_query_category with query: {query}")
    result: BaseMessage = chain.invoke(input={"query": query})

    logging.debug(f"Finished identify_query_category with result: {result}")
    return result
