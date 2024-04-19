from cpeq_infolettre_automatique.webscraper_io_client import WebscraperIoClient


class TestWebscraperIoClient:
    """Test Webscraper.io client."""

    @staticmethod
    def test_get_endpoint__should_do_this__when_in_this_situation() -> None:
        """Test that getting a page is successful."""
        client = WebscraperIoClient()
        response = client.get_endpoint("https://www.google.com")
        expected_response = {"status": "success", "data": "<html>...</html>"}
        assert response == expected_response

    @staticmethod
    def test_get_endpoint__should_do_this__when_in_this_other_situation() -> None:
        pass
