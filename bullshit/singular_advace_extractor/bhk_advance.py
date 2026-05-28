from typing import Literal

from pydantic import BaseModel, Field

from langchain_groq import ChatGroq

from langchain_core.prompts import ChatPromptTemplate

from langchain_core.runnables import (
    RunnableBranch,
    RunnableLambda,
    RunnableParallel,
    RunnablePassthrough
)

from langchain_core.output_parsers import PydanticOutputParser

from langchain.output_parsers import RetryOutputParser

from .GraphState import GraphState