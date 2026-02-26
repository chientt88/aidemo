import sqlite3
from datetime import datetime

DB_NAME = "assistant.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            role TEXT,
            content TEXT,
            timestamp TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_message(user_id, role, content):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
        INSERT INTO messages (user_id, role, content, timestamp)
        VALUES (?, ?, ?, ?)
    """, (user_id, role, content, datetime.now().isoformat()))

    conn.commit()
    conn.close()


def get_recent_messages(user_id, limit=6):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
        SELECT role, content FROM messages
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT ?
    """, (user_id, limit))

    rows = c.fetchall()
    conn.close()

    # đảo ngược để đúng thứ tự
    rows.reverse()

    return [{"role": role, "content": content} for role, content in rows]