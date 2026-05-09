import os
import sqlite3
from contextlib import contextmanager

@contextmanager
def get_connection():
    db_path = os.getenv("DB_PATH", "tasks.db")
    conn = sqlite3.connect(db_path)
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()
