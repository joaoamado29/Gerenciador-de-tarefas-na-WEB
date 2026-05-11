"""Camada de acesso a dados.

Concentra todo o SQL do projeto. A UI (``ui/*``) só chama estas funções,
nunca abre conexão direto. Facilita testar e trocar o banco depois.
"""

import pandas as pd

from database.connection import get_connection
from models.task import Task, TaskStatus


# --- Tabelas (categorias) -------------------------------------------------


def get_table_names() -> list[str]:
    """Lista os nomes das tabelas/categorias na ordem de criação."""
    with get_connection() as conn:
        cursor = conn.execute('SELECT name FROM tables ORDER BY id')
        return [r[0] for r in cursor.fetchall()]


def add_table(name: str) -> None:
    """Cria uma nova tabela/categoria.

    ``INSERT OR IGNORE`` evita erro caso o nome já exista (constraint UNIQUE).
    """
    with get_connection() as conn:
        conn.execute('INSERT OR IGNORE INTO tables (name) VALUES (?)', (name,))


def delete_table(name: str) -> None:
    """Remove a tabela e todas as tarefas associadas a ela.

    Apaga primeiro as tarefas (linhas filhas) e depois a tabela em si.
    """
    with get_connection() as conn:
        conn.execute('DELETE FROM tasks WHERE table_name = ?', (name,))
        conn.execute('DELETE FROM tables WHERE name = ?', (name,))


# --- Tarefas --------------------------------------------------------------


def add_task(table_name: str, name: str, status: TaskStatus, due_date: str) -> None:
    """Insere uma tarefa na tabela indicada.

    ``str(due_date)`` permite receber tanto ``str`` quanto ``datetime.date``
    (a UI passa um ``date`` vindo do ``st.date_input``).
    """
    with get_connection() as conn:
        conn.execute(
            'INSERT INTO tasks (table_name, name, status, due_date) VALUES (?, ?, ?, ?)',
            (table_name, name, status.value, str(due_date)),
        )


def get_tasks(table_name: str) -> list[Task]:
    """Retorna todas as tarefas de uma tabela."""
    with get_connection() as conn:
        cursor = conn.execute(
            'SELECT id, name, status, due_date FROM tasks WHERE table_name = ?',
            (table_name,),
        )
        rows = cursor.fetchall()
    return [Task(id=r[0], name=r[1], status=r[2], due_date=r[3]) for r in rows]


def get_tasks_by_status(table_name: str, status: TaskStatus) -> list[Task]:
    """Retorna as tarefas de uma tabela filtradas por status."""
    with get_connection() as conn:
        cursor = conn.execute(
            'SELECT id, name, status, due_date FROM tasks WHERE table_name = ? AND status = ?',
            (table_name, status.value),
        )
        rows = cursor.fetchall()
    return [Task(id=r[0], name=r[1], status=r[2], due_date=r[3]) for r in rows]


def delete_task(task_id: int) -> None:
    """Apaga uma tarefa pelo ID."""
    with get_connection() as conn:
        conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))


def set_completed(task_id: int) -> None:
    """Marca uma tarefa como concluída (status -> DONE)."""
    with get_connection() as conn:
        conn.execute(
            'UPDATE tasks SET status = ? WHERE id = ?',
            (TaskStatus.DONE.value, task_id),
        )


def tasks_to_dataframe(tasks: list[Task]) -> pd.DataFrame:
    """Converte uma lista de ``Task`` em ``DataFrame`` para exibir no Streamlit."""
    return pd.DataFrame(
        [(t.id, t.name, t.status, t.due_date) for t in tasks],
        columns=['ID', 'Tarefa', 'Status', 'Data'],
    )
