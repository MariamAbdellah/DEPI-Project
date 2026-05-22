from langchain_core.prompts import PromptTemplate
from llm import llm_model

cv_prompt = PromptTemplate(
    input_variables=["cv_text"],
    template="""You are an expert HR recruiter. Analyze this CV and provide:
1. A score out of 10
2. Key strengths (3 points)
3. Areas to improve (2 points)
4. Best fitting job role

CV:
{cv_text}

Analysis:"""
)

cv_chain = cv_prompt | llm_model

def run_cv_agent(cv_text: str) -> str:
    result = cv_chain.invoke({"cv_text": cv_text})
    # result is an AIMessage object, extract the text
    return result.content if hasattr(result, "content") else str(result)