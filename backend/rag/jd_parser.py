"""
Parses a raw, pasted job description into a structured list of requirements
using a Groq-hosted LLM via LangChain, with Pydantic enforcing the output shape.
"""

from typing import Literal
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

from app.config import GROQ_API_KEY, GROQ_MODEL
from .prompts import JD_EXTRACTION_SYSTEM_PROMPT


class Requirement(BaseModel):
    text: str = Field(description="Short, specific requirement phrase")
    category: Literal["must_have", "nice_to_have"]
    skill_area: str = Field(description="e.g. backend, ml, devops, frontend, soft_skill, domain_knowledge")


class ParsedJD(BaseModel):
    role_title: str = Field(description="The job title, inferred from the JD")
    seniority_level: Literal["entry", "mid", "senior"]
    requirements: list[Requirement]


def _get_llm():
    return ChatGroq(api_key=GROQ_API_KEY, model=GROQ_MODEL, temperature=0)


def parse_job_description(jd_text: str) -> ParsedJD:
    """
    Takes raw job description text, returns a ParsedJD with structured,
    categorized requirements. Uses structured output (not a hand-parsed
    JSON string) so a malformed LLM response fails loudly instead of
    silently producing garbage downstream.
    """
    llm = _get_llm().with_structured_output(ParsedJD)

    prompt = ChatPromptTemplate.from_messages([
        ("system", JD_EXTRACTION_SYSTEM_PROMPT),
        ("human", "{jd_text}"),
    ])

    chain = prompt | llm
    return chain.invoke({"jd_text": jd_text})