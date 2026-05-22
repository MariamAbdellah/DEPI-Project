# agents/job_agent.py
from langchain_core.prompts import PromptTemplate
from llm import llm_model

job_prompt = PromptTemplate(
    input_variables=["skills", "experience", "education"],
    template="""You are a career advisor. Based on this candidate profile, recommend 5 suitable job roles.
For each role explain why it fits and what skills match.

Skills: {skills}
Experience: {experience}
Education: {education}

Recommendations:"""
)

job_chain = job_prompt | llm_model

def run_job_agent(skills: str, experience: str, education: str) -> str:
    return job_chain.invoke({
        "skills": skills,
        "experience": experience,
        "education": education
    })