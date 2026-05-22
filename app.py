from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
from typing import Optional
from chat import chat_system
from db import create_tables
from utils.pdf_reader import extract_text_from_pdf
import tempfile, os, shutil, uuid

app = FastAPI()

# python -m uvicorn app:app --reload --port 8005 

@app.on_event("startup")
async def startup():
    create_tables()
    print("✅ Database table ready.")


session_contexts: dict[str, dict] = {}


class ChatRequest(BaseModel):
    user_id: str
    message: str

class ChatResponse(BaseModel):
    user_id: str
    reply: str


@app.post("/session/new")
async def new_session():
    """Generate a new user_id to use in all other endpoints."""
    return {"user_id": str(uuid.uuid4())}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    context = session_contexts.get(request.user_id, {})
    reply = chat_system(
        user_question=request.message,
        user_id=request.user_id,
        context=context
    )
    return {
        "user_id": request.user_id,
        "reply": reply,
    }


@app.post("/upload-cv")
async def upload_cv(
    user_id: str = Form(...),
    target_role: Optional[str] = Form(None),
    file: UploadFile = File(...)
):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    try:
        cv_text = extract_text_from_pdf(tmp_path)
    finally:
        os.unlink(tmp_path)

    session_contexts[user_id] = {
        "cv_text": cv_text,
        "role": target_role or "",
    }

    return {
        "status": "CV uploaded successfully",
        "user_id": user_id,
        "message": "You can now chat. Try: 'evaluate my cv', 'give me interview questions', or 'recommend jobs'."
    }


# @app.get("/history/{user_id}")
# async def get_history(user_id: str):
#     return {
#         "user_id": user_id,
#         "message_count": count_user_messages(user_id)
#     }