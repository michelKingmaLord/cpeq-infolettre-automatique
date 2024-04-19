"""Tests for the WebScraperIOClient and related functions."""

from decouple import config

from cpeq_infolettre_automatique.config import sitemaps
from cpeq_infolettre_automatique.utils import process_raw_response, save_data_to_json
from cpeq_infolettre_automatique.webscraper_io_client import WebScraperIoClient


class TestWebscraperIoClient:
    """Test Webscraper.io client."""

    @staticmethod
    def test_create_scraping_jobs() -> None:
        """Test creating scraping jobs using WebScraperIOClient.

        Ensures that the create_scraping_jobs method returns a list of job IDs.
        """
        client = WebScraperIoClient(api_token=config("WEBSCRAPER_IO_API_KEY"))
        sitemap_dicts = [{'sitemap_id': sitemap['sitemap_id']} for sitemap in sitemaps]
        job_ids = client.create_scraping_jobs(sitemap_dicts)
        assert isinstance(job_ids, list), "Expected job_ids to be a list"
        assert all(isinstance(id, str) for id in job_ids), "All job IDs should be strings"
        print("test_create_scraping_jobs passed")

    @staticmethod
    def test_get_endpoint__should_do_this__when_in_this_situation() -> None:
        """Test that getting a page is successful."""
        client = WebScraperIoClient()
        response = client.get_endpoint("https://www.google.com")
        expected_response = {"status": "success", "data": "<html>...</html>"}
        assert response == expected_response

    @staticmethod
    def test_get_endpoint__should_do_this__when_in_this_other_situation() -> None:
        """Test that getting a page is successful."""
        pass
