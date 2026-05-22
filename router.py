# router.py

def route(user_message: str) -> str:
    msg = user_message.lower()

    cv_keywords = ["cv", "resume", "my background", "my experience", 
                   "evaluate me", "assess my", "review my cv"]
    question_keywords = ["interview", "questions", "prepare", "ask me", 
                         "practice", "what will they ask"]
    job_keywords = ["job", "role", "recommend", "what suits me", 
                    "career", "apply", "positions", "opportunities"]

    if any(k in msg for k in cv_keywords):
        return "cv"
    if any(k in msg for k in question_keywords):
        return "questions"
    if any(k in msg for k in job_keywords):
        return "jobs"
    return "chat"   # default — just use your existing chat chain