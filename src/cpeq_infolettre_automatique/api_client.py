# Importations
import json

import httpx


# Variables Globales et Constantes
# API_TOKEN  = 'insert Token here'
api_token = 'insert Token here'

# SITEMAP_IDS
sitemaps = [
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
    }
]

# Test Variables

# Sitemaps tests
# sitemap_ids = ['1127309', '1120854', '1125386']  # List of sitemap IDs, FAQDD ne se trouvait rien et bloquait!
sitemap_ids = ["1125386"]

# Start Scraping job tests
new_scraping_job = 21417285  # unique scraping job test
all_scraping_jobs = ['21417285', '21416924', '21398005']  # multiple scraping job test

# Scraping Download and process scraping job tests
scraping_job_id = 21395222  # unique scraping job test
multiple_job_ids = ['21417285', '21416924', '21398005']   # multiple scraping job test

# Save to JSON tests
processed_scraping_job_id = 21398005  # unique scraping job test
processed_scraping_jobs_ids = ['21417285', '21416924', '21398005']  # multiple scraping job test

# Classes
class WebScraperIOClient:
    def __init__(self, api_token):
        self.api_token = api_token
        self.base_url = "https://api.webscraper.io/api/v1"
        self.headers = {'Content-Type': 'application/json'}

    def create_scraping_jobs(self, sitemap_ids):
        """Starts scraping jobs for multiple sitemap IDs and returns their job IDs."""
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
                print(f"Error starting job for sitemap {sitemap_id}: {str(e)}")
        return job_ids

    def get_scraping_job_details(self, scraping_job_id):
        """Retrieves details of a specific scraping job."""
        url = f"{self.base_url}/scraping-job/{scraping_job_id}?api_token={self.api_token}"
        try:
            response = httpx.get(url)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as error:
            return {"error": "HTTP error", "status_code": error.response.status_code, "details": str(error)}
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


# Initialisation du client
client = WebScraperIOClient(api_token)


# Methods
def process_raw_response(raw_response):
    """Converts raw JSON lines into a list of dictionaries (valid JSON array)."""
    try:
        data = [json.loads(line) for line in raw_response.strip().split('\n') if line.strip()]
        return data
    except json.JSONDecodeError as error:
        return {"error": "Failed to decode JSON", "details": str(error)}


def download_and_process_multiple_jobs(job_ids):
    """Converts raw JSON lines into a list of dictionaries (valid JSON array) and saves it into a dictionnary."""
    combined_data = []  # This will store all processed data

    for job_id in job_ids:
        print(f"Starting download for Job ID: {job_id}")
        data = client.download_scraping_job_data(job_id)
        if isinstance(data, list):  # Check if data retrieval was successful
            combined_data.extend(data)  # Add processed data to the combined list
            print(f"Processed data for job {job_id}:", data[:2] if len(data) > 2 else data)
        else:
            print(f"Error processing data for Job ID {job_id}: {data}")

    return combined_data


def save_data_to_json(data, file_path='output.json'):
    """Saves processed data to a JSON file."""
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        return f"Data successfully saved to {file_path}"
    except IOError as error:
        return {"error": "Failed to write to file", "details": str(error)}