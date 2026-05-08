from langchain.agents import initialize_agent, Tool
# embed jobs
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from llm import llm_model


def parse_cv(file):
    # Use NuExtract / IMCatalina
    return structured_json


# Tool 1: CV Evaluation
def evaluate_cv(input_text):
    prompt = f"""
    Evaluate this CV for a Data Scientist role:
    {input_text}

    Give:
    - Score out of 100
    - Strengths
    - Weaknesses
    """
    return llm.invoke(prompt)

# def evaluate_cv(cv_json, job_role):
#     # Prompt LLM
#     return {
#         "score": 78,
#         "strengths": [],
#         "weaknesses": []
#     }

# job recommender ################################# prompt or similarity search?
def recommend_jobs(cv_json):
    query = " ".join(cv_json["skills"])
    docs = vectorstore.similarity_search(query)
    return docs


# interview generator     /////will it need dataset?
def generate_questions(cv_json, job_role):
    prompt = f"""
    Generate technical + behavioral interview questions
    for {job_role} based on:
    {cv_json}
    """
    return llm_model(prompt)


# # Tool 2: Interview Questions
# def generate_questions(input_text):
#     prompt = f"""
#     Generate 5 interview questions for this candidate:
#     {input_text}
#     """
#     return llm_model.invoke(prompt)