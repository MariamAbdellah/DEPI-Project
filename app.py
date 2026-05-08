# POST /chat              # main chatbot interaction
# POST /upload-cv         # upload & parse CV
# GET  /jobs              # get recommendations
# POST /interview         # start interview session

from fastapi import FastAPI
from chat import chat_system, sum_msgs


fastAPI_APP = FastAPI()

#  uvicorn app:fastAPI_APP --reload --port 8005
from pydantic import BaseModel, Field

# class ChatRequest(BaseModel):
#     user_question: str = Field(..., example="مرحبا")
#     user_id: str = Field(..., example="fb1358d6-e72e-407e-ba4d-a88310c4c084")



@fastAPI_APP.post("/chat")
def chat():
    response = 0
    return {"response": response}

@fastAPI_APP.post("/upload_cv")
def upload_cv():
    response = 0
    return {"response": response}

@fastAPI_APP.get("/find_jobs")
def find_jobs():
    response = 0
    return {"response": response}


@fastAPI_APP.post("/interview")
def interview():
    response = 0
    return {"response": response}