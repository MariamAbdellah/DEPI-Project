import psycopg 
from langchain_postgres import PostgresChatMessageHistory
from config import CONN_STR
import uuid

connect_database = psycopg.connect(CONN_STR)
table_name = "chat_history"


def create_tables(table_name="chat_history"):
    PostgresChatMessageHistory.create_tables(connect_database, table_name)
    return f"Table {table_name} created successfully."


def _safe_uuid(user_id: str) -> str:
    """Convert any string to a valid UUID so Postgres never rejects it."""
    try:
        uuid.UUID(user_id)   # already a valid UUID, use as-is
        return user_id
    except ValueError:
        # deterministic: same input always gives same UUID
        return str(uuid.uuid5(uuid.NAMESPACE_DNS, user_id))


def get_history_from_postgres(user_id):
    history = PostgresChatMessageHistory(
        table_name,
        _safe_uuid(user_id),
        sync_connection=connect_database,
    )
    return history


def count_user_messages(user_id):
    query = f"""
    SELECT COUNT(*) 
    FROM {table_name}
    WHERE session_id = %s;
    """
    with connect_database.cursor() as cur:
        cur.execute(query, (_safe_uuid(user_id),))
        count = cur.fetchone()[0]
    return int(count / 2)