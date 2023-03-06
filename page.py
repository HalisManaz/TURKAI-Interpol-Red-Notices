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

    def notice_representation(self, notices: List[dict]) -> None:
        """
        Displays Interpol red notice information in a formatted manner.

        Args:
            notices (List[dict]): A list of dictionaries containing Interpol red notice information.

        Returns:
            None
        """
        for notice in notices:
            # Extract notice information from dictionary.
            forename: str = notice["forename"]
            name: str = notice["name"]
            entity_id: str = notice["entity_id"]
            nationality: str = notice["nationality"]
            age: int = notice["age"]
            image_url: str = notice["image_url"]

            # Display notice information in a formatted manner.
            st.markdown(
                f"""
        <div style="display: flex; flex-direction: column;">
            <a href="https://www.interpol.int/en/How-we-work/Notices/View-Red-Notices#{entity_id.replace("/", "-")}">
                <img src="{image_url}" width="184" height="238" />
            </a>
            <br>
            <p><strong>Notices Id:</strong> {entity_id}</p>
            <p><strong>Forename:</strong> {forename}</p>
            <p><strong>Name:</strong> {name}</p>
            <p><strong>Age:</strong> {age}</p>
            <p><strong>Nationality:</strong> {nationality}</p>
            <hr style='border: 2px solid gray'>
        </div>
        """,
                unsafe_allow_html=True,
            )

    def show_sidebar(self) -> None:
        """
        Displays the sidebar for filtering notices.
        """
        with st.sidebar:
            # Add input fields and select box for filtering notices.
            self.filter_notice_id = st.text_input("Notice Id")
            self.filter_forename = st.text_input("Forename")
            self.filter_name = st.text_input("Name")
            self.filter_nationality = st.selectbox(
                "Nationality",
                ["All"] + [country.alpha_2 for country in pycountry.countries],
            )
            self.filter()

