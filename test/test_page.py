from unittest.mock import patch

from page import StreamlitRedNotices


def test_notice_representation():
    srn = StreamlitRedNotices()
    notices = [
        {
            "forename": "John",
            "name": "Doe",
            "entity_id": "2021/1010",
            "nationality": "US",
            "age": 30,
            "image_url": "https://path/to/image",
        }
    ]
    with patch("streamlit.markdown") as mock_markdown:
        srn.notice_representation(notices)
        mock_markdown.assert_called_once_with(
            f"""
    <div style="display: flex; flex-direction: column;">
        <a href="https://www.interpol.int/en/How-we-work/Notices/View-Red-Notices#2021-1010">
            <img src="https://path/to/image" width="184" height="238" />
        </a>
        <br>
        <p><strong>Notices Id:</strong> 2021/1010</p>
        <p><strong>Forename:</strong> John</p>
        <p><strong>Name:</strong> Doe</p>
        <p><strong>Age:</strong> 30</p>
        <p><strong>Nationality:</strong> US</p>
        <hr style='border: 2px solid gray'>
    </div>
    """,
            unsafe_allow_html=True,
        )
