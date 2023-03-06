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

    def filter(self) -> None:
        """
        Filters notices based on user input.
        """
        if st.button("Filter", type="primary"):
            if self.filter_notice_id:
                st.session_state.filter["entity_id"] = self.filter_notice_id

            elif self.filter_forename:
                st.session_state.filter["forename"] = self.filter_forename

            elif self.filter_name:
                st.session_state.filter["name"] = self.filter_name

            elif self.filter_nationality and self.filter_nationality != "All":
                st.session_state.filter["nationality"] = self.filter_nationality
            else:
                st.session_state.filter = {}

    def show_notices(self, notices: List[dict]) -> None:
        """
        Displays Interpol red notices in a formatted manner.

        Args:
            notices (List[dict]): A list of dictionaries containing Interpol red notice information.

        Returns:
            None
        """
        # Display the notices in columns
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            self.notice_representation(notices[0::4])
        with col2:
            self.notice_representation(notices[1::4])
        with col3:
            self.notice_representation(notices[2::4])
        with col4:
            self.notice_representation(notices[3::4])

    def show_page(self):
        """
        Shows the Streamlit page.
        """
        # Show the sidebar
        self.show_sidebar()
        # Show the updated date and time
        st.markdown(
            f"""<h3 style='text-align: center;'>
            Updated from {datetime.datetime.now().strftime("at %H:%M on %Y/%m/%d")}
            </h3>""",
            unsafe_allow_html=True,
        )

        # Show the Alerts and Red Notices headers
        st.markdown(
            "<h1 style='text-align: center;'> Alerts⚠️</h1>", unsafe_allow_html=True
        )
        alert_notices = self.mongo.find(filter={"alert": True})
        st.markdown(
            f"""<h4> {len(alert_notices)} alerts are founded</h4>""",
            unsafe_allow_html=True,
        )

        self.show_notices(alert_notices)
        st.markdown("---")
        st.markdown(
            "<h1 style='text-align: center;'> Red Notices🚨</h1>", unsafe_allow_html=True
        )

        # Get notices from MongoDB database with filter
        notices = self.mongo.find(filter=st.session_state.filter)
        # Show the number of notices found
        st.markdown(
            f"""<h4> {len(notices)} notices are founded</h4>""", unsafe_allow_html=True
        )

        # Display the notices in pages of 20 items each
        page_num = st.selectbox(
            "Page",
            [page_num for page_num in range(1, (len(notices) // 20) + 2)],
        )

        # Display the notices in columns
        notices = notices[(page_num - 1) * 20 : page_num * 20]
        self.show_notices(notices)


def main():
    show_red_notices = StreamlitRedNotices()
    show_red_notices.show_page()


if __name__ == "__main__":
    main()
