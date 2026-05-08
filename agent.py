
# LLM calls the tools based on prompt:  “Can you recommend jobs for me?” --> recommend_jobs(cv_json)

from llm import llm_model
from langchain.agents import initialize_agent, Tool
from langchain.llms import HuggingFacePipeline
from transformers import pipeline

Tool(  #descriptions are very important
    name="CV Parser",
    func=parse_cv,
    description="Use this when you need to extract structured information from a CV file"
)

Tool(
    name="Job Recommender",
    func=recommend_jobs,
    description="Use this when the user asks for job suggestions"
)

Tool(
    name="Interview Generator",
    func=generate_questions,
    description="Use this when the user wants interview questions"
)


tools = [
    Tool(name="CV Parser", func=parse_cv, description="Parse CV"),
    Tool(name="Evaluator", func=evaluate_cv, description="Evaluate CV"),
    Tool(name="Job Recommender", func=recommend_jobs, description="Recommend jobs"),
    Tool(name="Interview Generator", func=generate_questions, description="Generate interview questions"),
]

agent = initialize_agent(
    tools,
    llm_model,
    agent="structured-chat-zero-shot-react-description",
    verbose=True
)

