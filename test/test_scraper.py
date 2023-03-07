from scraper import Scraper


def test_organize_notices_data():
    scraper = Scraper()
    notices = [
        {
            "entity_id": "2022/1234",
            "forename": "John",
            "name": "Doe",
            "date_of_birth": "1985/02/28",
            "nationalities": ["US"],
            "_links": {"thumbnail": {"href": "https://example.com/image.jpg"}},
        },
        {
            "entity_id": "2022/5678",
            "forename": "Jane",
            "name": "Smith",
            "date_of_birth": "1995/07/12",
            "nationalities": None,
            "_links": {},
        },
    ]
    expected_result = [
        {
            "entity_id": "2022/1234",
            "forename": "John",
            "name": "Doe",
            "record_year": 2022,
            "record_id": 1234,
            "age": 38,
            "nationality": "US",
            "image_url": "https://example.com/image.jpg",
            "alert": True,
        },
        {
            "entity_id": "2022/5678",
            "forename": "Jane",
            "name": "Smith",
            "record_year": 2022,
            "record_id": 5678,
            "age": 28,
            "nationality": "Unknown",
            "image_url": "https://www.interpol.int/bundles/interpolfront/images/photo-not-available.png",
            "alert": True,
        },
    ]
    result = scraper.organize_notices_data(notices)
    assert result == expected_result
