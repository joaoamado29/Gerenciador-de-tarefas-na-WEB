"""Criação do schema do banco.

Roda automaticamente no início do app (ver ``app.py``).
"""

from database.connection import get_connection


def init_db() -> None:
    """Cria as tabelas ``tables`` e ``tasks`` se ainda não existirem.

    - ``tables``: catálogo das tabelas/categorias cadastradas pelo usuário
      (ex.: "Obrigacoes", "Lazer"). Nome é único.
    - ``tasks``: tarefas em si, ligadas a uma ``tables.name`` por
      ``table_name`` (relação simples, sem FK declarada).
    """
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
