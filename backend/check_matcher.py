from rag.matcher import analyze_job_fit

sample_jd = """
We are hiring a Backend Developer with 2+ years of experience in Python and REST API design.
Experience with Docker and containerization is a big plus. Familiarity with PostgreSQL required.
Must be comfortable working in a fast-paced startup environment. Experience with machine learning
is a bonus but not required.
"""

report = analyze_job_fit(sample_jd)

print(f"{report.role_title} ({report.seniority_level}) — Fit score: {report.overall_fit_score}/100\n")
for m in report.matches:
    print(f"[{m.category}] {m.requirement}")
    print(f"  match: {m.match_level}  evidence: {m.matched_evidence}")
    if m.drafted_bullet:
        print(f"  bullet: {m.drafted_bullet}")
    print(f"  why: {m.reasoning}\n")