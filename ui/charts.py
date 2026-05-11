"""Gráfico de distribuição de tarefas por status."""

import pandas as pd
import streamlit as st

from models.task import Task


def render_status_chart(tasks: list[Task]) -> None:
    """Mostra um gráfico de barras com a contagem por status.

    Não renderiza nada quando não há tarefas (evita um gráfico vazio
    embaixo da mensagem "Nenhuma tarefa encontrada").
    """
    if not tasks:
        return

    # value_counts() agrupa por status; o wrap em DataFrame de 1 linha
    # transforma os status em colunas, que é o formato que st.bar_chart
    # espera para gerar uma barra por categoria.
    status_counts = (
        pd.DataFrame([(t.status,) for t in tasks], columns=['Status'])['Status']
        .value_counts()
    )
    st.bar_chart(pd.DataFrame([status_counts.to_dict()]))
