import requests
import logging
from log.logging_config import setup_logging  # Updated import path

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

def fetch_data():
    base_url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
    pub_start_date = "2023-11-08T00:00:00.000Z"
    pub_end_date = "2024-01-05T23:59:59.999Z"
    url = f"{base_url}?pubStartDate={pub_start_date}&pubEndDate={pub_end_date}"

    try:
        logger.info(f"Fetching data from URL: {url}")
        response = requests.get(url)

        if response.status_code == 200:
            logger.info("Data fetched successfully.")
            return response.json()
        else:
            logger.warning(f"Failed to fetch data: {response.status_code}")
            return None
    except Exception as e:
        logger.error("Error occurred while fetching data.", exc_info=True)
        raise e
