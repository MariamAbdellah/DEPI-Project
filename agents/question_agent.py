# agents/question_agent.py
from langchain_core.prompts import PromptTemplate
from llm import llm_model

question_prompt = PromptTemplate(
    input_variables=["role", "skills"],
    template="""Generate 8 interview questions for a {role} candidate with skills in {skills}.
Include technical, behavioral, and situational questions. Number each one.

Questions:"""
)

question_chain = question_prompt | llm_model

def run_question_agent(role: str, skills: str) -> str:
    result = question_chain.invoke({"role": role, "skills": skills})
    return result.content if hasattr(result, "content") else str(result)