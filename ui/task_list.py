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
    if 'filtro_ativo' not in st.session_state:
        st.session_state.filtro_ativo = None

    tasks = get_tasks()

    if not tasks:
        st.write('Nenhuma tarefa encontrada')
        return tasks

    if st.session_state.filtro_ativo:
        displayed = get_tasks_by_status(TaskStatus(st.session_state.filtro_ativo))
    else:
        displayed = tasks

    st.dataframe(tasks_to_dataframe(displayed), hide_index=True)

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
