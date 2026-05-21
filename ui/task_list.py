"""Área principal: lista de tarefas, ações e filtro por status."""

import streamlit as st

from models.task import Task, TaskStatus
from repositories.task_repository import (
    delete_task,
    get_tasks,
    get_tasks_by_status,
    set_completed,
    tasks_to_dataframe,
)


def render_task_list() -> list[Task]:
    """Renderiza a tabela de tarefas e os botões de ação.

    Retorna **todas** as tarefas da tabela atual (não filtradas) para que
    o gráfico de status considere o total, não apenas o que está visível.
    """
    # filtro_ativo é persistido no session_state para sobreviver aos reruns
    # disparados pelos botões. None = sem filtro.
    if 'filtro_ativo' not in st.session_state:
        st.session_state.filtro_ativo = None

    # 'selected_table' é definido na sidebar (ui/sidebar.py).
    table_name = st.session_state.get('selected_table')
    if not table_name:
        st.write('Selecione uma tabela na barra lateral.')
        return []

    tasks = get_tasks(table_name)

    if not tasks:
        st.write('Nenhuma tarefa encontrada')
        return tasks

    # Aplica filtro só na visualização; 'tasks' segue completo para o gráfico.
    if st.session_state.filtro_ativo:
        displayed = get_tasks_by_status(table_name, TaskStatus(st.session_state.filtro_ativo))
    else:
        displayed = tasks

    st.dataframe(tasks_to_dataframe(displayed), hide_index=True, width='stretch')

    # Formato "ID. Nome" para conseguir extrair o ID com split('.') depois.
    selected = st.selectbox('Selecione a tarefa', [f"{t.id}. {t.name}" for t in tasks])

    left, mid, right = st.columns(3)

    if left.button("Tarefa Concluída", width="stretch"):
        task_id = int(selected.split('.')[0])
        set_completed(task_id)
        st.success("Tarefa marcada como concluída!")
        st.rerun()

    if mid.button('Deletar', width="stretch", type="primary"):
        task_id = int(selected.split('.')[0])
        delete_task(task_id)
        st.rerun()

    # menu_button devolve o item selecionado (ou None se nada foi clicado).
    aux_filter = right.menu_button(
        'Filtrar',
        options=[TaskStatus.DONE.value, TaskStatus.PENDING.value, "Todos"],
        width="stretch",
    )
    if aux_filter == "Todos":
        st.session_state.filtro_ativo = None
        st.rerun()
    elif aux_filter in (TaskStatus.DONE.value, TaskStatus.PENDING.value):
        st.session_state.filtro_ativo = aux_filter
        st.rerun()

    return tasks
