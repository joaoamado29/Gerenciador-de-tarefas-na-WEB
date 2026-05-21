"""Ponto de entrada do Gerenciador de Tarefas.

Executar com:
    streamlit run app.py
"""

from pathlib import Path

import streamlit as st

from database.migrations import init_db
from ui.charts import render_status_chart
from ui.sidebar import render_sidebar
from ui.task_list import render_task_list
from ui.rodape import rodape_text

# Garante que o schema do SQLite exista antes de qualquer interação.
init_db()

_CSS_PATH = Path(__file__).parent / "static" / "style.css"


def _inject_css() -> None:
    st.markdown(f"<style>{_CSS_PATH.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)


def main() -> None:
    """Monta a página principal do app (título, sidebar, lista, gráfico, rodapé)."""
    _inject_css()
    st.title('Gerenciador RAD')
    render_sidebar()
    tasks = render_task_list()
    render_status_chart(tasks)
    rodape_text()


if __name__ == "__main__":
    main()
