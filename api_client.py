import requests
import logging


logger = logging.getLogger(__name__)


def get_json_data(url: str):
    """
    Fetches JSON data from a dummy API endpoint.
    
    Args:
        url: The API endpoint URL
    
    Returns:
        list: Parsed JSON data from the API response
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise exception for bad status codes
        data = response.json()
        logger.info("Successfully fetched %d items from API: %s", len(data), url)
        return data
    except requests.exceptions.RequestException as e:
        logger.error("Error fetching data from API: %s", e)
        return None
