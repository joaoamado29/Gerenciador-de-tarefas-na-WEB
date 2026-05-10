from database.connection import get_connection

DEFAULT_TABLES = ('Obrigacoes', 'Lazer', 'Projetos')


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

        cols = [r[1] for r in conn.execute('PRAGMA table_info(tasks)').fetchall()]
        if 'table_name' not in cols:
            conn.execute(
                "ALTER TABLE tasks ADD COLUMN table_name TEXT NOT NULL DEFAULT 'Obrigacoes'"
            )

        for default in DEFAULT_TABLES:
            conn.execute('INSERT OR IGNORE INTO tables (name) VALUES (?)', (default,))
