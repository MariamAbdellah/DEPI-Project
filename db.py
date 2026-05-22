import psycopg 
from langchain_postgres import PostgresChatMessageHistory
from config import CONN_STR
import uuid
import json
from datetime import datetime, timezone

# Add autocommit=True so every write is immediately saved
connect_database = psycopg.connect(CONN_STR, autocommit=True)
table_name = "chat_history"


def create_tables(table_name="chat_history"):
    PostgresChatMessageHistory.create_tables(connect_database, table_name)
    return f"Table {table_name} created successfully."


def _safe_uuid(user_id: str) -> str:
    try:
        uuid.UUID(user_id)
        return user_id
    except ValueError:
        return str(uuid.uuid5(uuid.NAMESPACE_DNS, user_id))


def get_history_from_postgres(user_id):
    history = PostgresChatMessageHistory(
        table_name,
        _safe_uuid(user_id),
        sync_connection=connect_database,
    )
    return history



def save_message(user_id: str, role: str, content: str):
    # """Manually save a single message to the database."""
    query = f"""
    INSERT INTO {table_name} (session_id, message)
    VALUES (%s, %s);
    """

    
    message = json.dumps({
        "type": role,  # "human" or "ai"
        "content": content,
        "created_at": datetime.now(timezone.utc).isoformat()
    })
    
    with connect_database.cursor() as cur:
        cur.execute(query, (_safe_uuid(user_id), message))
    connect_database.commit()


def get_messages(user_id: str) -> list[dict]:
    # """Retrieve all messages for a user."""
    query = f"""
    SELECT message FROM {table_name}
    WHERE session_id = %s
    ORDER BY id ASC;
    """
    import json
    with connect_database.cursor() as cur:
        cur.execute(query, (_safe_uuid(user_id),))
        rows = cur.fetchall()
    return [json.loads(row[0]) for row in rows]