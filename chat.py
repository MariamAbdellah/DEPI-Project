from llm import llm_model
from prompts import full_prompt
from db import get_history_from_postgres
from router import route
from agents.cv_agent import run_cv_agent
from agents.question_agent import run_question_agent
from agents.job_agent import run_job_agent
from langchain_core.runnables.history import RunnableWithMessageHistory

chat_chain = full_prompt | llm_model

chat_with_history_postgres = RunnableWithMessageHistory(
    chat_chain,
    get_history_from_postgres,
    input_message_key="user_question",
    history_messages_key="History"
)


def chat_system(user_question: str, user_id: str, context: dict = None) -> str:
    intent = route(user_question)
    context = context or {}

    if intent == "cv" and context.get("cv_text"):
        agent_response = run_cv_agent(context["cv_text"])
        followup = f"I analyzed your CV. Here's what I found:\n\n{agent_response}\n\nFeel free to ask me anything about the results."
        return _save_and_return(followup, user_question, user_id)

    if intent == "questions":
        role = context.get("role", "Software Engineer")
        skills = context.get("skills", "general programming")
        agent_response = run_question_agent(role, skills)
        followup = f"Here are your interview questions for a {role} role:\n\n{agent_response}"
        return _save_and_return(followup, user_question, user_id)

    if intent == "jobs":
        agent_response = run_job_agent(
            skills=context.get("skills", "not provided"),
            experience=context.get("experience", "not provided"),
            education=context.get("education", "not provided")
        )
        followup = f"Based on your profile, here are my job recommendations:\n\n{agent_response}"
        return _save_and_return(followup, user_question, user_id)

    # Default: general chat
    result = chat_with_history_postgres.invoke(
        {"user_question": user_question},
        config={"configurable": {"session_id": user_id}}
    )
    # extract text from AIMessage
    return result.content if hasattr(result, "content") else str(result)


def _save_and_return(agent_response: str, original_question: str, user_id: str) -> str:
    chat_with_history_postgres.invoke(
        {"user_question": f"[Agent Result] {original_question}\n\nResult: {agent_response}"},
        config={"configurable": {"session_id": user_id}}
    )
    return agent_response


import re

def _clean_response(text: str) -> str:
    """Remove markdown formatting for plain text readability."""
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)   # **bold** → bold
    text = re.sub(r'\*(.*?)\*', r'\1', text)         # *italic* → italic
    text = re.sub(r'#{1,6}\s*', '', text)            # ## headings → plain
    text = re.sub(r'✅|⚠️|🔹|💡|>', '', text)       # remove emojis/symbols
    text = re.sub(r'\n{3,}', '\n\n', text)           # collapse extra newlines
    return text.strip()