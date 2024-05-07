"""Main script for initiating web scraping jobs and processing their data."""

from cpeq_infolettre_automatique.config import sitemaps
from cpeq_infolettre_automatique.utils import process_raw_response, save_data_to_json
from cpeq_infolettre_automatique.webscraper_io_client import WebScraperIoClient
from vector_store import VectorStore  # Ensure VectorStore is correctly imported


def main() -> None:
    """Main function to initiate web scraping jobs and process their data."""
    client = WebScraperIoClient()
    sitemap_ids = [sitemap["sitemap_id"] for sitemap in sitemaps]
    job_ids = client.create_scraping_jobs(sitemap_ids)

    for job_id in job_ids:
        raw_data = client.download_scraping_job_data(job_id)
        processed_data = process_raw_response(raw_data)
        if processed_data:
            save_message = save_data_to_json(processed_data, f"{job_id}_output.json")
            print(save_message)


if __name__ == "__main__":
    main()

# Ancien code utilisants les embedded rubrics split3
# Incertitude car le test devrait utiliser download multiple scraping_job data.
# if __name__ == "__main__":
#     client = WebScraperIoClient()
#     sitemap_ids = [sitemap["sitemap_id"] for sitemap in sitemaps]
#     job_ids = client.create_scraping_jobs(sitemap_ids)
#     vector_store = VectorStore("embedded_rubrics_split3.json")  # Assuming embeddings are prepared and saved in this file

#     for job_id in job_ids:
#         raw_data = client.download_scraping_job_data(job_id)
#         processed_data = process_raw_response(raw_data)
#         if processed_data:
#             save_message = save_data_to_json(processed_data, f"{job_id}_output.json")
#             print(save_message)
