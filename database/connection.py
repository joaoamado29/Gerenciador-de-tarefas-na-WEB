"""Conexão com o banco SQLite.

Centraliza a abertura/fechamento da conexão para o restante do projeto
não precisar lidar com `sqlite3` diretamente.
"""

import os
import sqlite3
from contextlib import contextmanager


@contextmanager
def get_connection():
    """Context manager que devolve uma conexão SQLite.

    - Caminho do banco vem da variável de ambiente ``DB_PATH``
      (default: ``tasks.db`` no diretório atual). Os testes usam essa
      variável para apontar para um banco temporário.
    - Faz ``commit`` automaticamente ao sair do bloco ``with`` sem erro.
    - Sempre fecha a conexão, mesmo se houver exceção.
    """
    db_path = os.getenv("DB_PATH", "tasks.db")
    conn = sqlite3.connect(db_path)
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()
