"""Tests for the WebScraperIOClient and related functions."""

from typing import Any

import pytest
from decouple import config

# from cpeq_infolettre_automatique.config import sitemaps
from cpeq_infolettre_automatique.utils import process_raw_response, save_data_to_json
from cpeq_infolettre_automatique.webscraper_io_client import WebScraperIoClient


sitemaps: list[dict[str, str]] = [
    {
        "name": "Ciraig",
        "url": "https://ciraig.org/index.php/fr/category/actualites/",
        "sitemap_id": "1127309",
    },
    {
        "name": "CIRODD",
        "url": "https://cirodd.org/actualites/",
        "sitemap_id": "1120854",
    },
    {
        "name": "FAQDD",
        "url": "https://faqdd.qc.ca/publications/",
        "sitemap_id": "1120853",
    },
    {
        "name": "ECPAR",
        "url": "http://www.ecpar.org/fr/nouvelles/",
        "sitemap_id": "1125386",
    },
]

# Sitemaps tests
# sitemap_ids = [
#     "1127309",
#     "1120854",
#     "1125386",
# ]  
# List of sitemap IDs, FAQDD ne se trouvait rien et bloquait!
# sitemap_ids = ["1125386"]

# Start Scraping job tests
new_scraping_job = 21417285  # unique scraping job test
all_scraping_jobs = ["21417285", "21416924", "21398005"]  # multiple scraping job test

# Scraping Download and process scraping job tests
scraping_job_id = 21395222  # unique scraping job test
multiple_job_ids = ["21417285", "21416924", "21398005"]  # multiple scraping job test

# Save to JSON tests
processed_scraping_job_id = 21398005  # unique scraping job test
processed_scraping_jobs_ids = ["21417285", "21416924", "21398005"]  # multiple scraping job test


class TestWebscraperIoClient:
    """Test Webscraper.io client."""

    # @pytest.skip("reason here")
    @staticmethod
    def test_create_scraping_jobs() -> None:
        """Test creating scraping jobs using WebScraperIOClient.

        Ensures that the create_scraping_jobs method returns a list of job IDs.
        """
        client = WebScraperIoClient(api_token=config("WEBSCRAPER_IO_API_KEY"))
        job_ids = client.create_scraping_jobs(sitemaps)
        assert isinstance(job_ids, list), "Expected job_ids to be a list"
        assert all(isinstance(id, str) for id in job_ids), "All job IDs should be strings"
        print("test_create_scraping_jobs passed")

    # @staticmethod
    # def test_get_endpoint__should_do_this__when_in_this_situation() -> None:
    #     """Test that getting a page is successful."""
    #     client = WebScraperIoClient()
    #     response = client.get_endpoint("https://www.google.com")
    #     expected_response = {"status": "success", "data": "<html>...</html>"}
    #     assert response == expected_response

    # @staticmethod
    # def test_get_endpoint__should_do_this__when_in_this_other_situation() -> None:
    #     """Test that getting a page is successful."""
    #     pass
