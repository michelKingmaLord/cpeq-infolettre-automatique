"""Main script for initiating web scraping jobs and processing their data."""

from config import sitemaps
from utils import process_raw_response, save_data_to_json
from webscraper_io_client import WebScraperIOClient


# Incertitude car le test devrait utiliser download multiple scraping_job data.
if __name__ == "__main__":
    client = WebScraperIOClient()
    sitemap_ids = [sitemap["sitemap_id"] for sitemap in sitemaps]
    job_ids = client.create_scraping_jobs(sitemap_ids)
    for job_id in job_ids:
        raw_data = client.download_scraping_job_data(job_id)
        processed_data = process_raw_response(raw_data)
        if processed_data:
            save_message = save_data_to_json(processed_data, f"{job_id}_output.json")
            print(save_message)
