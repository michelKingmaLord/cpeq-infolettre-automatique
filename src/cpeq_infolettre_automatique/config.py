"""Configuration and constants for the web scraping client."""
API_TOKEN = "insert Token here"  # noqa: S105

sitemaps: list[dict[str, str, str]] = [
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
# sitemap_ids = ['1127309', '1120854', '1125386']  # List of sitemap IDs, FAQDD ne se trouvait rien et bloquait!
sitemap_ids = ["1125386"]

# Start Scraping job tests
new_scraping_job = 21417285  # unique scraping job test
all_scraping_jobs = ["21417285", "21416924", "21398005"]  # multiple scraping job test

# Scraping Download and process scraping job tests
scraping_job_id = 21395222  # unique scraping job test
multiple_job_ids = ["21417285", "21416924", "21398005"]  # multiple scraping job test

# Save to JSON tests
processed_scraping_job_id = 21398005  # unique scraping job test
processed_scraping_jobs_ids = ["21417285", "21416924", "21398005"]  # multiple scraping job test
