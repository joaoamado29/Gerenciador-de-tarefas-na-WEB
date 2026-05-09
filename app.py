import streamlit as st

from database.migrations import init_db
from ui.charts import render_status_chart
from ui.sidebar import render_sidebar
from ui.task_list import render_task_list
from ui.rodape import rodape_text

init_db()


def main() -> None:
    st.title('Gerenciador RAD')
    render_sidebar()
    tasks = render_task_list()
    render_status_chart(tasks)
    rodape_text()

if __name__ == "__main__":
    main()
