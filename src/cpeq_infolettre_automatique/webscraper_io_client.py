"""Client module for WebScraper.io API interaction."""
import httpx
from decouple import config

from cpeq_infolettre_automatique.config import sitemaps
from cpeq_infolettre_automatique.utils import process_raw_response


class WebscraperIoClientTest:
    """A client example for interacting with the WebScraper.io API."""

    def get_endpoint(self, url: str) -> dict:
        response = httpx.get(url)
        return self._handle_response(response)

    def _handle_response(self, response):
        pass


class WebScraperIoClient:
    """A client for interacting with the WebScraper.io API.

    This class provides methods to create scraping jobs,
    retrieve job details, and download job data.
    """

    def __init__(self, api_token: str):
        """Initialize the WebScraperIOClient with the provided API token."""
        self.api_token = config("WEBSCRAPER_IO_API_KEY")
        self.base_url: str = "https://api.webscraper.io/api/v1"
        self.headers: dict[str, str] = {"Content-Type": "application/json"}

    def create_scraping_jobs(self, sitemap_ids: list[dict[str, str, str]]) -> list[str]:
        """Starts scraping jobs for multiple sitemap IDs and returns their scraping job IDs."""
        job_ids = []
        for sitemap_id in sitemap_ids:
            url = f"{self.base_url}/scraping-job"
            data = {
                "sitemap_id": sitemap_id,
                "driver": "fulljs",
                "page_load_delay": 3000,
                "request_interval": 3000,
            }
            try:
                response = httpx.post(
                    url,
                    json=data,
                    headers=self.headers,
                    params={"api_token": self.api_token},
                )
                response.raise_for_status()
                job_id = response.json().get("data", {}).get("id")
                if job_id:
                    job_ids.append(job_id)
                    print(f"Job {job_id} started for sitemap {sitemap_id}")
                else:
                    print(f"No job ID received for sitemap {sitemap_id}")
            except Exception as e:
                print(f"Error starting scraping job for sitemap {sitemap_id}: {str(e)}")
        return job_ids

    def get_scraping_job_details(self, scraping_job_id):
        """Retrieves details of a specific scraping job."""
        url = f"{self.base_url}/scraping-job/{scraping_job_id}?api_token={self.api_token}"
        try:
            response = httpx.get(url)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as error:
            return {
                "error": "HTTP error",
                "status_code": error.response.status_code,
                "details": str(error),
            }
        except httpx.RequestError as error:
            return {"error": "Request error", "details": str(error)}

    def download_scraping_job_data(self, scraping_job_id):
        """Fetches raw JSON data for a scraping job and processes it into a structured format."""
        url = f"{self.base_url}/scraping-job/{scraping_job_id}/json?api_token={self.api_token}"
        try:
            response = httpx.get(url)
            response.raise_for_status()
            return process_raw_response(response.text)
        except Exception as error:
            return {"error": "Failed to process data", "details": str(error)}

    def download_and_process_multiple_jobs(self, job_ids):
        """Converts raw JSON lines into a list of dictionaries (valid JSON array) and saves it into a dictionnary."""
        combined_data = []  # This will store all processed data

        for job_id in job_ids:
            print(f"Starting download for Job ID: {job_id}")
            data = self.download_scraping_job_data(job_id)
            if isinstance(data, list):  # Check if data retrieval was successful
                combined_data.extend(data)  # Add processed data to the combined list
                print(f"Processed data for job {job_id}:", data[:2] if len(data) > 2 else data)
            else:
                print(f"Error processing data for Job ID {job_id}: {data}")

        return combined_data
