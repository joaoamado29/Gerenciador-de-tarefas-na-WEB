import os
import pytest

from database.migrations import init_db
from models.task import TaskStatus
from repositories.task_repository import (
    add_task,
    delete_task,
    get_table_names,
    get_tasks,
    get_tasks_by_status,
    set_completed,
)

TABLE = "Obrigacoes"


@pytest.fixture(autouse=True)
def setup_db(tmp_path):
    os.environ["DB_PATH"] = str(tmp_path / "test.db")
    init_db()
    yield
    del os.environ["DB_PATH"]


def test_default_tables_seeded():
    assert get_table_names() == ["Obrigacoes", "Lazer", "Projetos"]


def test_add_and_get_task():
    add_task(TABLE, "Estudar Python", TaskStatus.PENDING, "2025-12-01")
    tasks = get_tasks(TABLE)
    assert len(tasks) == 1
    assert tasks[0].name == "Estudar Python"
    assert tasks[0].status == TaskStatus.PENDING.value


def test_tasks_isolated_per_table():
    add_task("Obrigacoes", "Reuniao", TaskStatus.PENDING, "2025-12-01")
    add_task("Lazer", "Cinema", TaskStatus.PENDING, "2025-12-02")
    assert len(get_tasks("Obrigacoes")) == 1
    assert len(get_tasks("Lazer")) == 1
    assert len(get_tasks("Projetos")) == 0


def test_delete_task():
    add_task(TABLE, "Tarefa temporária", TaskStatus.PENDING, "2025-12-01")
    task_id = get_tasks(TABLE)[0].id
    delete_task(task_id)
    assert get_tasks(TABLE) == []


def test_set_completed():
    add_task(TABLE, "Fazer relatório", TaskStatus.PENDING, "2025-12-01")
    task_id = get_tasks(TABLE)[0].id
    set_completed(task_id)
    tasks = get_tasks(TABLE)
    assert tasks[0].status == TaskStatus.DONE.value


def test_filter_by_status():
    add_task(TABLE, "Pendente 1", TaskStatus.PENDING, "2025-12-01")
    add_task(TABLE, "Pendente 2", TaskStatus.PENDING, "2025-12-02")
    add_task(TABLE, "Concluída", TaskStatus.DONE, "2025-12-03")
    pending = get_tasks_by_status(TABLE, TaskStatus.PENDING)
    done = get_tasks_by_status(TABLE, TaskStatus.DONE)
    assert len(pending) == 2
    assert len(done) == 1
