from dataclasses import dataclass
from enum import Enum


class TaskStatus(str, Enum):
    PENDING = "Pendente"
    DONE = "Concluido"


@dataclass
class Task:
    id: int
    name: str
    status: str
    due_date: str
