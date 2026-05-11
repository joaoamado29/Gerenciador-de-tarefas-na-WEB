from database.connection import get_connection


def init_db() -> None:
    with get_connection() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS tables (
                id   INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT    NOT NULL UNIQUE
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                table_name TEXT    NOT NULL,
                name       TEXT    NOT NULL,
                status     TEXT    NOT NULL,
                due_date   TEXT    NOT NULL
            )
        ''')
