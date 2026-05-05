import os
import pytest

os.environ["DB_PATH"] = ":memory:"

from database.migrations import init_db
from models.task import Task, TaskStatus
from repositories.task_repository import (
    add_task,
    delete_task,
    get_tasks,
    get_tasks_by_status,
    set_completed,
)


@pytest.fixture(autouse=True)
def setup_db():
    init_db()
    yield
    # banco em memória é descartado automaticamente


def test_add_and_get_task():
    add_task("Estudar Python", TaskStatus.PENDING, "2025-12-01")
    tasks = get_tasks()
    assert len(tasks) == 1
    assert tasks[0].name == "Estudar Python"
    assert tasks[0].status == TaskStatus.PENDING.value


def test_delete_task():
    add_task("Tarefa temporária", TaskStatus.PENDING, "2025-12-01")
    task_id = get_tasks()[0].id
    delete_task(task_id)
    assert get_tasks() == []


def test_set_completed():
    add_task("Fazer relatório", TaskStatus.PENDING, "2025-12-01")
    task_id = get_tasks()[0].id
    set_completed(task_id)
    tasks = get_tasks()
    assert tasks[0].status == TaskStatus.DONE.value


def test_filter_by_status():
    add_task("Pendente 1", TaskStatus.PENDING, "2025-12-01")
    add_task("Pendente 2", TaskStatus.PENDING, "2025-12-02")
    add_task("Concluída", TaskStatus.DONE, "2025-12-03")
    pending = get_tasks_by_status(TaskStatus.PENDING)
    done = get_tasks_by_status(TaskStatus.DONE)
    assert len(pending) == 2
    assert len(done) == 1
