import os
import sqlite3
from contextlib import contextmanager

DB_PATH = os.getenv("DB_PATH", "tasks.db")


@contextmanager
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()
