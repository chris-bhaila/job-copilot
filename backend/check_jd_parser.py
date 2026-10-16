from rag.jd_parser import parse_job_description

sample_jd = """
We are hiring a Backend Developer with 2+ years of experience in Python and REST API design.
Experience with Docker and containerization is a big plus. Familiarity with PostgreSQL required.
Must be comfortable working in a fast-paced startup environment. Experience with machine learning
is a bonus but not required.
"""

result = parse_job_description(sample_jd)
print(result.role_title, "-", result.seniority_level)
for req in result.requirements:
    print(f"[{req.category}] ({req.skill_area}) {req.text}")