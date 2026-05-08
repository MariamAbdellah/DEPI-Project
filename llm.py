# llm setup
from langchain.llms import HuggingFacePipeline

from transformers import pipeline

# pipe = pipeline(
#     "text-generation",
#     model="Qwen/Qwen2.5-7B-Instruct",
#     max_new_tokens=512
# )

# llm = HuggingFacePipeline(pipeline=pipe)



from langchain_openai import ChatOpenAI

from config import HF_T, MODEL,BASE_URL

llm_model = ChatOpenAI(model=MODEL
                 , api_key=HF_T
                 ,base_url=BASE_URL
                 ,temperature=0.2)