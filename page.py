import datetime
from typing import List

import pycountry
import streamlit as st

from db import MongoDB


class StreamlitRedNotices:
    def __init__(self) -> None:
        """
        Initializes StreamlitRedNotices object.
        """
        # Set Streamlit page configuration.
        st.set_page_config(
            page_title="Interpol Red Notices",
            page_icon="🔎",
            layout="wide",
            initial_sidebar_state="expanded",
        )
        # Add CSS styling.
        st.markdown(
            """
        <style>
            div.block-container {padding-top:1rem;}
        </style>
        """,
            unsafe_allow_html=True,
        )
        # Set session_state variable for filtering notices.
        if "filter" not in st.session_state:
            st.session_state.filter = {}
        # Initialize MongoDB object for database access.
        self.mongo = MongoDB()
