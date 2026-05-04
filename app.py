import streamlit as st
import pandas as pd
import sqlite3
import time

def init_db():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            status TEXT NOT NULL,
            due_date TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_task(name, status, due_date):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tasks (name, status, due_date)
        VALUES (?, ?, ?)
    ''', (name, status, due_date))
    conn.commit()
    conn.close()

def get_tasks():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM tasks
    ''')
    
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def delete_task(id):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM tasks WHERE id = ?
    ''', (id,))
    conn.commit()
    conn.close()

def main():
    st.title('Gerenciador RAD')
    init_db()

    # MENU LATERAL
    name = st.sidebar.text_input('Tarefa', placeholder='Digite a tarefa')
    status = st.sidebar.selectbox('Status', ('Pendente', 'Concluido'))
    date = st.sidebar.date_input('Data')
    
    if st.sidebar.button('Adicionar'):
        if name:
            add_task(name, status, date)
            st.sidebar.success("Tarefa adicionada com sucesso")
        else:
            st.sidebar.error("Algo deu errado! Dê um nome a Tarefa. ")

    # AREA PRINCIPAL
    tasks = get_tasks()
    if tasks:
        df = pd.DataFrame(tasks, columns=['ID', 'Tarefa', 'Status', 'Data'])
        st.dataframe(df, hide_index=True)
    else:
        st.write('Nenhuma tarefa encontrada')

    # SELETÃO E BOTÃO DE DELEÇÃO

    selected = st.selectbox('Selecione a tarefa', [f"{t[0]}. {t[1]}" for t in get_tasks()])

    left, mid, right = st.columns(3)

    if left.button("Tarefa Concluída", width="stretch"):
        pass

    if mid.button('Filtrar', width="stretch"):
        pass
    
    if right.button('Deletar', width="stretch", type="primary"):
        task_id = int(selected.split('.')[0])
        delete_task(task_id)
        st.rerun()


    
main()