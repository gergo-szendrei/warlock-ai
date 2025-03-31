import logging
import os

from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field


class Classification(BaseModel):
    politics: int = Field(
        description="""
        Describes if the passage is related to politics in any way (either present or historical), 
        Presence of political figures, acts or ideologies means relation to politics,
        0 means no relation to politics,
        1 means it is related to politics,
        Be strict in your decision
        """
    )
    terrorism: int = Field(
        description="""
        Describes if the passage is related to terrorism in any way (either present or historical), 
        Presence of terrorist figures, acts or ideologies means relation to politics,
        0 means no relation to terrorism,
        1 means it is related to terrorism,
        Be strict in your decision
        """
    )
    pornography: int = Field(
        description="""
        Describes if the passage is related to pornography in any way, 
        Presence of pornographic figures, acts or ideologies means relation to politics,
        0 means no relation to pornography AND it is safe for people under age 18,
        1 means it is related to pornography OR it is not safe/recommended for people under age 18,
        Be strict in your decision
        """
    )


model = (ChatOllama(
    model=os.environ["LLM_MODEL"],
    base_url=os.environ["LLM_BASE_URL"],
    temperature=float(os.environ["LLM_TEMPERATURE"]))
         .with_structured_output(Classification))

base_prompt = """
    Extract the desired information from the following passage.
    Only extract the properties mentioned in the 'Classification' function.
    Passage:
    {passage}
    """

prompt = PromptTemplate(
    input_variables=["passage"],
    template=base_prompt
)

chain = prompt | model


def identify_impure_thoughts(query: str) -> dict | Classification:
    logging.debug(f"Calling identify_impure_thoughts with query: {query}")
    result: dict | Classification = chain.invoke(input={"passage": query})

    logging.debug(f"Finished identify_impure_thoughts with result: {result}")
    return result
