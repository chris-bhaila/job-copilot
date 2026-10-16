"""
Core matching logic: for each parsed JD requirement, retrieves relevant
resume chunks and asks the LLM to judge the match -- grounded strictly in
retrieved evidence, never inventing experience that isn't there.
"""

from typing import Literal, Optional
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

from app.config import GROQ_API_KEY, GROQ_MODEL
from .jd_parser import Requirement, parse_job_description
from .vectorstore import retrieve
from .prompts import MATCH_SYSTEM_PROMPT


class LLMMatchJudgment(BaseModel):
    """Only the fields the LLM actually needs to judge -- the requirement
    text and category are already known to us, so we don't ask the model
    to regenerate them (which is exactly what caused the schema error)."""
    match_level: Literal["strong", "partial", "none"]
    matched_evidence: Optional[str] = Field(
        default=None,
        description="Name of the project/experience entry that supports this, or null if none",
    )
    drafted_bullet: Optional[str] = Field(
        default=None,
        description="A resume bullet grounded in retrieved evidence; null if match_level is 'none'",
    )
    reasoning: str = Field(description="One sentence explaining the match_level decision")


class MatchResult(BaseModel):
    """The full, combined result -- known fields (requirement, category)
    plus the LLM's judgment, assembled in Python."""
    requirement: str
    category: Literal["must_have", "nice_to_have"]
    match_level: Literal["strong", "partial", "none"]
    matched_evidence: Optional[str] = None
    drafted_bullet: Optional[str] = None
    reasoning: str


class JobFitReport(BaseModel):
    role_title: str
    seniority_level: str
    overall_fit_score: float = Field(
        description="0-100 weighted score, must_have requirements count more than nice_to_have"
    )
    matches: list[MatchResult]


def _get_llm():
    return ChatGroq(api_key=GROQ_API_KEY, model=GROQ_MODEL, temperature=0)


def _match_single_requirement(requirement: Requirement) -> MatchResult:
    """
    Retrieve resume context for one requirement and ask the LLM to judge
    the match against ONLY that retrieved context -- never the full resume,
    which keeps the grounding honest and auditable per-requirement.
    """
    retrieved_chunks = retrieve(requirement.text, top_k=3)
    context = "\n\n---\n\n".join(
        f"[{c['metadata']['name']}]\n{c['text']}" for c in retrieved_chunks
    )

    llm = _get_llm().with_structured_output(LLMMatchJudgment)
    prompt = ChatPromptTemplate.from_messages([
        ("system", MATCH_SYSTEM_PROMPT),
        ("human", (
            "Requirement: {requirement_text}\n"
            "Category: {category}\n\n"
            "Retrieved resume context (the ONLY evidence you may use):\n{context}"
        )),
    ])

    chain = prompt | llm
    judgment: LLMMatchJudgment = chain.invoke({
        "requirement_text": requirement.text,
        "category": requirement.category,
        "context": context,
    })

    # Guardrail: enforce the schema's own rule even if the LLM slips --
    # a "none" match should never carry a drafted bullet.
    drafted_bullet = judgment.drafted_bullet if judgment.match_level != "none" else None

    return MatchResult(
        requirement=requirement.text,
        category=requirement.category,
        match_level=judgment.match_level,
        matched_evidence=judgment.matched_evidence,
        drafted_bullet=drafted_bullet,
        reasoning=judgment.reasoning,
    )


def _compute_fit_score(matches: list[MatchResult]) -> float:
    """Weighted score: must_have requirements count 2x nice_to_have.
    strong=1.0, partial=0.5, none=0.0 per requirement."""
    level_score = {"strong": 1.0, "partial": 0.5, "none": 0.0}
    weight = {"must_have": 2.0, "nice_to_have": 1.0}

    total_weight = sum(weight[m.category] for m in matches)
    if total_weight == 0:
        return 0.0

    earned = sum(level_score[m.match_level] * weight[m.category] for m in matches)
    return round((earned / total_weight) * 100, 1)


def analyze_job_fit(jd_text: str) -> JobFitReport:
    """Full pipeline: parse the JD, match each requirement independently
    against retrieved resume evidence, compute an overall fit score."""
    parsed = parse_job_description(jd_text)
    matches = [_match_single_requirement(req) for req in parsed.requirements]
    fit_score = _compute_fit_score(matches)

    return JobFitReport(
        role_title=parsed.role_title,
        seniority_level=parsed.seniority_level,
        overall_fit_score=fit_score,
        matches=matches,
    )