# HR Multi-Agent System 🤖

An AI-powered HR assistant that analyzes CVs, generates interview questions, and recommends job roles — built with LangChain, FastAPI, and PostgreSQL.

---

## What It Does

- **CV Analysis** — upload a PDF CV and get a score, strengths, and areas to improve
- **Interview Questions** — generates tailored interview questions based on the candidate's profile
- **Job Recommendations** — recommends suitable job roles based on skills and experience
- **Chat History** — stores every conversation in PostgreSQL so history is never lost

---

## Project Structure

```
DEPI Project/
├── app.py              ← FastAPI endpoints
├── chat.py             ← Main agent logic + routing
├── db.py               ← PostgreSQL connection + save/load messages
├── llm.py              ← HuggingFace LLM setup
├── prompts.py          ← LangChain prompt templates
├── router.py           ← Intent detection (cv / questions / jobs / chat)
├── config.py           ← Loads environment variables
├── .env                ← Your secret keys (never share this)
├── requirements.txt
├── agents/
│   ├── cv_agent.py         ← CV scoring and feedback
│   ├── question_agent.py   ← Interview question generation
│   └── job_agent.py        ← Job role recommendation
└── utils/
    └── pdf_reader.py       ← Extracts text from PDF files
```

---

## Setup

### 1. Clone the project and create a virtual environment

```bash
git clone <your-repo-url>
cd "DEPI Project"

python -m venv penv
penv\Scripts\activate        # Windows
source penv/bin/activate     # Mac/Linux
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create your `.env` file

Create a file named `.env` in the project root with the following:

```env
HF_TOKEN=your_huggingface_token_here
MODEL=Qwen/Qwen3-Coder-Next:novita
BASE_URL=https://router.huggingface.co/v1
CONN_STR=postgresql://username:password@localhost:5432/your_database_name
```

- `HF_TOKEN` — get yours from [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
- `CONN_STR` — your PostgreSQL connection string. Replace `username`, `password`, and `your_database_name` with your actual values.

### 4. Set up PostgreSQL

Make sure PostgreSQL is installed and running, then create a database:

```sql
CREATE DATABASE hr_agent;
```

The table is created automatically when you start the server — you don't need to create it manually.

### 5. Start the server

```bash
python -m uvicorn app:app --reload --port 8005
```

The API will be running at `http://127.0.0.1:8005`  
Interactive docs (Swagger UI) at `http://127.0.0.1:8005/docs`

---

## How to Use

### Step 1 — Get a session ID
```
POST /session/new
```
Copy the `user_id` from the response. Use it in all other requests.

### Step 2 — Upload your CV (optional)
```
POST /upload-cv
  user_id:     paste your user_id
  target_role: Data Scientist     (optional)
  file:        your_cv.pdf
```

### Step 3 — Chat
```
POST /chat
{
  "user_id": "your-user-id-here",
  "message": "evaluate my cv"
}
```

**Trigger phrases:**
| What you want | What to say |
|---|---|
| CV analysis | "evaluate my cv", "review my resume", "assess my background" |
| Interview questions | "give me interview questions", "help me prepare", "practice interview" |
| Job recommendations | "recommend jobs", "what role suits me", "career advice" |
| General chat | anything else |

### Step 4 — View history
```
GET /history/{user_id}
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/session/new` | Generate a new user ID |
| `POST` | `/chat` | Send a message to the HR chatbot |
| `POST` | `/upload-cv` | Upload a PDF CV |
| `GET` | `/history/{user_id}` | Get message count for a user |
| `GET` | `/docs` | Swagger UI (interactive API docs) |

---

## How the Agent Routing Works

```
User message
     ↓
router.py — detects intent
     ↓
"cv"        → cv_agent.py       (needs CV uploaded first)
"questions" → question_agent.py
"jobs"      → job_agent.py
"chat"      → general LangChain conversation with memory
     ↓
Response saved to PostgreSQL + in-memory history
```

---

## Notes

- Chat history is stored **both** in memory (fast, for active session) and in PostgreSQL (persistent, survives restarts)
- The `user_id` must be kept consistent across requests — use `/session/new` to generate one
- CV context (uploaded PDF) is stored in memory only — if the server restarts, re-upload the CV
- The model is accessed via the HuggingFace Inference API, so no GPU is required on your machine
