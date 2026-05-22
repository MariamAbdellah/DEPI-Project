# # from llm import llm_model
# # from prompts import full_prompt
# # from db import get_history_from_postgres
# # from router import route
# # from agents.cv_agent import run_cv_agent
# # from agents.question_agent import run_question_agent
# # from agents.job_agent import run_job_agent
# # from langchain_core.runnables.history import RunnableWithMessageHistory

# # chat_chain = full_prompt | llm_model

# # chat_with_history_postgres = RunnableWithMessageHistory(
# #     chat_chain,
# #     get_history_from_postgres,
# #     input_message_key="user_question",
# #     history_messages_key="History"
# # )


# # def chat_system(user_question: str, user_id: str, context: dict = None) -> str:
# #     intent = route(user_question)
# #     context = context or {}

# #     if intent == "cv" and context.get("cv_text"):
# #         agent_response = run_cv_agent(context["cv_text"])
# #         followup = f"I analyzed your CV. Here's what I found:\n\n{agent_response}\n\nFeel free to ask me anything about the results."
# #         return _save_and_return(followup, user_question, user_id)

# #     if intent == "questions":
# #         role = context.get("role", "Software Engineer")
# #         skills = context.get("skills", "general programming")
# #         agent_response = run_question_agent(role, skills)
# #         followup = f"Here are your interview questions for a {role} role:\n\n{agent_response}"
# #         return _save_and_return(followup, user_question, user_id)

# #     if intent == "jobs":
# #         agent_response = run_job_agent(
# #             skills=context.get("skills", "not provided"),
# #             experience=context.get("experience", "not provided"),
# #             education=context.get("education", "not provided")
# #         )
# #         followup = f"Based on your profile, here are my job recommendations:\n\n{agent_response}"
# #         return _save_and_return(followup, user_question, user_id)

# #     # Default: general chat
# #     result = chat_with_history_postgres.invoke(
# #         {"user_question": user_question},
# #         config={"configurable": {"session_id": user_id}}
# #     )
# #     # extract text from AIMessage
# #     return result.content if hasattr(result, "content") else str(result)


# # def _save_and_return(agent_response: str, original_question: str, user_id: str) -> str:
# #     chat_with_history_postgres.invoke(
# #         {"user_question": f"[Agent Result] {original_question}\n\nResult: {agent_response}"},
# #         config={"configurable": {"session_id": user_id}}
# #     )
# #     return agent_response


# # import re

# # def _clean_response(text: str) -> str:
# #     """Remove markdown formatting for plain text readability."""
# #     text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)   # **bold** → bold
# #     text = re.sub(r'\*(.*?)\*', r'\1', text)         # *italic* → italic
# #     text = re.sub(r'#{1,6}\s*', '', text)            # ## headings → plain
# #     text = re.sub(r'✅|⚠️|🔹|💡|>', '', text)       # remove emojis/symbols
# #     text = re.sub(r'\n{3,}', '\n\n', text)           # collapse extra newlines
# #     return text.strip()



# from llm import llm_model
# from prompts import full_prompt
# from db import get_history_from_postgres, save_message, get_messages
# from router import route
# from agents.cv_agent import run_cv_agent
# from agents.question_agent import run_question_agent
# from agents.job_agent import run_job_agent
# from langchain_core.messages import HumanMessage, AIMessage
# import re

# chat_chain = full_prompt | llm_model


# def _clean_response(text: str) -> str:
#     text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
#     text = re.sub(r'\*(.*?)\*', r'\1', text)
#     text = re.sub(r'#{1,6}\s*', '', text)
#     text = re.sub(r'✅|⚠️|🔹|💡|>', '', text)
#     text = re.sub(r'\n{3,}', '\n\n', text)
#     return text.strip()


# def _build_history(user_id: str) -> list:
#     """Load past messages from DB and convert to LangChain message objects."""
#     messages = get_messages(user_id)
#     history = []
#     for msg in messages:
#         if msg["type"] == "human":
#             history.append(HumanMessage(content=msg["content"]))
#         else:
#             history.append(AIMessage(content=msg["content"]))
#     return history


# def chat_system(user_question: str, user_id: str, context: dict = None) -> str:
#     intent = route(user_question)
#     context = context or {}

#     # ── Specialist agents ──────────────────────────────────────────────────
#     if intent == "cv" and context.get("cv_text"):
#         agent_response = _clean_response(run_cv_agent(context["cv_text"]))
#         reply = f"I analyzed your CV. Here's what I found:\n\n{agent_response}\n\nFeel free to ask me anything about the results."

#     elif intent == "questions":
#         role = context.get("role", "Software Engineer")
#         skills = context.get("skills", "general programming")
#         agent_response = _clean_response(run_question_agent(role, skills))
#         reply = f"Here are your interview questions for a {role} role:\n\n{agent_response}"

#     elif intent == "jobs":
#         agent_response = _clean_response(run_job_agent(
#             skills=context.get("skills", "not provided"),
#             experience=context.get("experience", "not provided"),
#             education=context.get("education", "not provided")
#         ))
#         reply = f"Based on your profile, here are my job recommendations:\n\n{agent_response}"

#     else:
#         # ── General chat — load history from DB and invoke ─────────────────
#         history = _build_history(user_id)
#         result = chat_chain.invoke({
#             "user_question": user_question,
#             "History": history
#         })
#         reply = result.content if hasattr(result, "content") else str(result)

#     # ── Save both messages to DB manually ─────────────────────────────────
#     save_message(user_id, "human", user_question)
#     save_message(user_id, "ai", reply)

#     return reply



from typing import Dict
from langchain_openai import ChatOpenAI
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from prompts import full_prompt
from db import save_message, get_messages
from router import route
from agents.cv_agent import run_cv_agent
from agents.question_agent import run_question_agent
from agents.job_agent import run_job_agent
from config import HF_T, MODEL, BASE_URL
import re

llm_model = ChatOpenAI(
    model=MODEL,
    api_key=HF_T,
    base_url=BASE_URL,
    temperature=0.2,
)

chat_chain = full_prompt | llm_model

# ── In-memory store (your class code) ─────────────────────────────────────
_STORE: Dict[str, Dict] = {}

def _ensure_session(session_id: str):
    if session_id not in _STORE:
        _STORE[session_id] = {
            "lc_history": InMemoryChatMessageHistory(),
            "raw_history": []
        }
    return _STORE[session_id]

def get_history(session_id: str):
    return _ensure_session(session_id)["lc_history"]

chat_with_memory = RunnableWithMessageHistory(
    chat_chain,
    get_history,
    input_messages_key="user_question",
    history_messages_key="History",
)


# ── Helpers ────────────────────────────────────────────────────────────────
def _clean_response(text: str) -> str:
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    text = re.sub(r'#{1,6}\s*', '', text)
    text = re.sub(r'✅|⚠️|🔹|💡|>', '', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


# ── Main entry point ───────────────────────────────────────────────────────
def chat_system(user_question: str, user_id: str, context: dict = None) -> str:
    user_question = (user_question or "").strip()
    if not user_question:
        return "اكتب رسالة أولاً."

    intent = route(user_question)
    context = context or {}
    sess = _ensure_session(user_id)

    # ── Specialist agents ──────────────────────────────────────────────────
    if intent == "cv" and context.get("cv_text"):
        agent_response = _clean_response(run_cv_agent(context["cv_text"]))
        reply = f"I analyzed your CV. Here's what I found:\n\n{agent_response}\n\nFeel free to ask me anything about the results."

    elif intent == "questions":
        role = context.get("role", "Software Engineer")
        skills = context.get("skills", "general programming")
        agent_response = _clean_response(run_question_agent(role, skills))
        reply = f"Here are your interview questions for a {role} role:\n\n{agent_response}"

    elif intent == "jobs":
        agent_response = _clean_response(run_job_agent(
            skills=context.get("skills", "not provided"),
            experience=context.get("experience", "not provided"),
            education=context.get("education", "not provided")
        ))
        reply = f"Based on your profile, here are my job recommendations:\n\n{agent_response}"

    else:
        # ── General chat with in-memory history (your class code) ──────────
        msg = chat_with_memory.invoke(
            {"user_question": user_question},
            config={"configurable": {"session_id": user_id}}
        )
        reply = msg.content

    # ── Save to in-memory raw_history (your class code) ────────────────────
    sess["raw_history"].append({"role": "human", "content": user_question})
    sess["raw_history"].append({"role": "ai", "content": reply})

    # ── Save to Postgres (new addition) ────────────────────────────────────
    save_message(user_id, "human", user_question)
    save_message(user_id, "ai", reply)

    return reply


def get_raw_history(session_id: str) -> list[dict]:
    return list(_ensure_session(session_id)["raw_history"])


def clear_session(session_id: str) -> None:
    _STORE[session_id] = {
        "lc_history": InMemoryChatMessageHistory(),
        "raw_history": []
    }