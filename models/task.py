"""Modelos de domínio (tarefa e status)."""

from dataclasses import dataclass
from enum import Enum


class TaskStatus(str, Enum):
    """Status possíveis de uma tarefa.

    Herda de ``str`` para que o valor (``"Pendente"`` / ``"Concluido"``)
    seja gravado direto no SQLite sem conversão manual.
    """

    PENDING = "Pendente"
    DONE = "Concluido"


@dataclass
class Task:
    """Representa uma linha da tabela ``tasks``.

    ``status`` e ``due_date`` ficam como ``str`` porque o SQLite não tem
    tipos nativos para enum/data — a conversão fica no consumidor.
    """

    id: int
    name: str
    status: str
    due_date: str
