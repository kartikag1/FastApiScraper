import requests
import logging
import os
from bs4 import BeautifulSoup
from tenacity import retry, wait_fixed, stop_after_attempt

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@retry(wait=wait_fixed(5), stop=stop_after_attempt(3))
def fetch_url_with_retry(url, headers=None, proxies=None):
    response = requests.get(url, headers=headers, proxies=proxies)
    response.raise_for_status()
    return response.content

def parse_product_details(soup, selectors):
    """Extract product details from the BeautifulSoup object."""
    title = soup.find(selectors["product_title"]['tag'], class_=selectors["product_title"]['class']).text.strip()
    image_url = soup.find(selectors["product_image"]['tag'], class_=selectors["product_image"]['class']).find('img')['src']
    return {"product_title": title.replace("\u2013", "-"), "product_image": image_url}

def download_image(image_url, save_dir):
    """Download an image from a URL and save it locally."""
    try:
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        
        image_name = os.path.basename(image_url)
        save_path = os.path.join(save_dir, image_name)

        response = requests.get(image_url)
        response.raise_for_status()

        with open(save_path, 'wb') as file:
            file.write(response.content)
        
        logger.info(f"Downloaded image: {save_path}")
        return save_path
    except Exception as e:
        logger.error(f"Failed to download image {image_url}: {e}")
        return None
