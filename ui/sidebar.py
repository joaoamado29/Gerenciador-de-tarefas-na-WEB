import streamlit as st

from models.task import TaskStatus
from repositories.task_repository import add_task, get_table_names


def render_sidebar() -> None:
    tables = get_table_names()
    table_name = st.sidebar.selectbox('Tabela', tables, key='selected_table')
    name = st.sidebar.text_input('Tarefa', placeholder='Digite a tarefa')
    status = st.sidebar.selectbox('Status', [s.value for s in TaskStatus])
    date = st.sidebar.date_input('Data')

    if st.sidebar.button('Adicionar'):
        if not table_name:
            st.sidebar.error("Selecione uma tabela.")
        elif name:
            add_task(table_name, name, TaskStatus(status), date)
            st.sidebar.success("Tarefa adicionada com sucesso")
        else:
            st.sidebar.error("Dê um nome à tarefa.")

    # TODO: botão "Nova tabela" usando repositories.task_repository.add_table
