"""Barra lateral: criação de tarefas e gerenciamento de tabelas."""

import streamlit as st

from models.task import TaskStatus
from repositories.task_repository import (
    add_table,
    add_task,
    delete_table,
    get_table_names,
)


def render_sidebar() -> None:
    """Renderiza a sidebar com dois expanders: Tarefas e Tabelas."""

    st.sidebar.header('Gerenciador de Tarefas', divider='gray')
    st.sidebar.write('')

    tables = get_table_names()

    # --- Expander Tarefas: adicionar uma tarefa nova ---------------------
    with st.sidebar.expander('**Tarefas**', expanded=False):
        # A chave 'selected_table' é lida em ui/task_list.py para saber
        # qual tabela exibir na área principal.
        table_name = st.selectbox('Tabela', tables, key='selected_table')
        name = st.text_input('Tarefa', placeholder='Digite a tarefa')
        status = st.selectbox('Status', [s.value for s in TaskStatus])
        date = st.date_input('Data')

        if st.button('Adicionar', key='btn_add_task', width="stretch"):
            if not table_name:
                st.error('Selecione uma tabela.')
            elif name:
                add_task(table_name, name, TaskStatus(status), date)
                st.success('Tarefa adicionada com sucesso')
            else:
                st.error('Dê um nome à tarefa.')

    # --- Expander Tabela: criar / deletar categorias ---------------------
    with st.sidebar.expander('**Tabela**', expanded=False):
        new_table = st.text_input(
            'Nova tabela', placeholder='Nome da tabela', key='new_table_name'
        )
        if st.button('Criar', key='btn_create_table', width="stretch"):
            if new_table.strip():
                add_table(new_table.strip())
                st.success(f'Tabela "{new_table.strip()}" criada.')
                # rerun para o selectbox de tabelas refletir a nova entrada.
                st.rerun()
            else:
                st.error('Dê um nome à tabela.')

        table_to_delete = st.selectbox(
            'Deletar tabela', tables, key='table_to_delete'
        )
        if st.button('Deletar', key='btn_delete_table', width="stretch", type="primary"):
            if table_to_delete:
                delete_table(table_to_delete)
                st.success(f'Tabela "{table_to_delete}" excluída.')
                st.rerun()
            else:
                st.error('Selecione uma tabela.')
