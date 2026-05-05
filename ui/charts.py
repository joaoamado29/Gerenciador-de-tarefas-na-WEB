import pandas as pd
import streamlit as st

from models.task import Task


def render_status_chart(tasks: list[Task]) -> None:
    if not tasks:
        return

    status_counts = (
        pd.DataFrame([(t.status,) for t in tasks], columns=['Status'])['Status']
        .value_counts()
    )
    st.bar_chart(pd.DataFrame([status_counts.to_dict()]))
