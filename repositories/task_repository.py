import pandas as pd

from database.connection import get_connection
from models.task import Task, TaskStatus


def get_table_names() -> list[str]:
    with get_connection() as conn:
        cursor = conn.execute('SELECT name FROM tables ORDER BY id')
        return [r[0] for r in cursor.fetchall()]


def add_table(name: str) -> None:
    with get_connection() as conn:
        conn.execute('INSERT OR IGNORE INTO tables (name) VALUES (?)', (name,))


def delete_table(name: str) -> None:
    with get_connection() as conn:
        conn.execute('DELETE FROM tasks WHERE table_name = ?', (name,))
        conn.execute('DELETE FROM tables WHERE name = ?', (name,))


def add_task(table_name: str, name: str, status: TaskStatus, due_date: str) -> None:
    with get_connection() as conn:
        conn.execute(
            'INSERT INTO tasks (table_name, name, status, due_date) VALUES (?, ?, ?, ?)',
            (table_name, name, status.value, str(due_date)),
        )


def get_tasks(table_name: str) -> list[Task]:
    with get_connection() as conn:
        cursor = conn.execute(
            'SELECT id, name, status, due_date FROM tasks WHERE table_name = ?',
            (table_name,),
        )
        rows = cursor.fetchall()
    return [Task(id=r[0], name=r[1], status=r[2], due_date=r[3]) for r in rows]


def get_tasks_by_status(table_name: str, status: TaskStatus) -> list[Task]:
    with get_connection() as conn:
        cursor = conn.execute(
            'SELECT id, name, status, due_date FROM tasks WHERE table_name = ? AND status = ?',
            (table_name, status.value),
        )
        rows = cursor.fetchall()
    return [Task(id=r[0], name=r[1], status=r[2], due_date=r[3]) for r in rows]


def delete_task(task_id: int) -> None:
    with get_connection() as conn:
        conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))


def set_completed(task_id: int) -> None:
    with get_connection() as conn:
        conn.execute(
            'UPDATE tasks SET status = ? WHERE id = ?',
            (TaskStatus.DONE.value, task_id),
        )


def tasks_to_dataframe(tasks: list[Task]) -> pd.DataFrame:
    return pd.DataFrame(
        [(t.id, t.name, t.status, t.due_date) for t in tasks],
        columns=['ID', 'Tarefa', 'Status', 'Data'],
    )
