import streamlit as st
def rodape_text():
    st.markdown(
        """
        <style>
        .footer {
            text-align: center;
            color: #888;
            font-size: 0.8rem;
            margin-top: 2rem;
            padding-top: 1rem;
            border-top: 1px solid #e0e0e0;
        }
        .footer a { color: #888; text-decoration: none; }
        .footer a:hover { color: #555; text-decoration: underline; }
        </style>
        <div class="footer">
            © 2026 · <a href="https://github.com/joaoamado29" target="_blank">github - @joaoamado29</a>
        </div>
        """,
        unsafe_allow_html=True,
    )
