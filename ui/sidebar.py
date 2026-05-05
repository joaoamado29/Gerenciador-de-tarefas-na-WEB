import streamlit as st

from models.task import TaskStatus
from repositories.task_repository import add_task


def render_sidebar() -> None:
    name = st.sidebar.text_input('Tarefa', placeholder='Digite a tarefa')
    status = st.sidebar.selectbox('Status', [s.value for s in TaskStatus])
    date = st.sidebar.date_input('Data')

    if st.sidebar.button('Adicionar'):
        if name:
            add_task(name, TaskStatus(status), date)
            st.sidebar.success("Tarefa adicionada com sucesso")
        else:
            st.sidebar.error("Dê um nome à tarefa.")
