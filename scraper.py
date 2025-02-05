import os
import json
import logging
import time
from requests.adapters import HTTPAdapter
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from config import CONFIG
from utils import fetch_url_with_retry, parse_product_details, download_image
from data_storage import DataStorage

class Scraper:
    def __init__(self, proxy=None, max_retries=3, use_cache=True):
        self.proxy = proxy
        self.max_retries = max_retries
        self.logger = logging.getLogger(__name__)
        self.data_storage = DataStorage(use_cache=use_cache)

    def scrape_product_details(self, product_url):
        """Scrape product details from an individual product page."""
        attempt = 0
        while attempt < self.max_retries:
            content = fetch_url_with_retry(product_url, CONFIG["HEADERS"], {"http": self.proxy, "https": self.proxy} if self.proxy else None)
            if content:
                details = parse_product_details(BeautifulSoup(content, 'html.parser'), CONFIG["SELECTORS"])
                if details.get("product_image"):
                    details["local_image_path"] = download_image(details["product_image"], 'static/images')
                return details
            attempt += 1
            time.sleep(2)  # Wait 2 seconds before retrying
        return {}

    def scrape_page(self, page_number):
        cached_data = self.data_storage.get_cached_data(page_number)
        if cached_data:
            self.logger.info(f"Cache hit for page {page_number}")
            return cached_data
        
        url = CONFIG["BASE_URL"].format(page_number)
        content = fetch_url_with_retry(url, CONFIG["HEADERS"], {"http": self.proxy, "https": self.proxy} if self.proxy else None)
        
        if not content:
            return []

        soup = BeautifulSoup(content, 'html.parser')
        products = soup.find_all(CONFIG["SELECTORS"]["product_list"]['tag'], class_=CONFIG["SELECTORS"]["product_list"]['class'])
        
        scraped_data = []
        
        for product in products:
            title_tag = product.find(CONFIG["SELECTORS"]["product_link"]['tag'], class_=CONFIG["SELECTORS"]["product_link"]['class'])
            link_tag = title_tag.find('a') if title_tag else None
            
            if link_tag and 'href' in link_tag.attrs:
                product_link = urljoin(url, link_tag['href'])
                price_tag = product.find(CONFIG["SELECTORS"]["price"]['tag'], class_=CONFIG["SELECTORS"]["price"]['class'])
                product_price = float(price_tag.text.strip().replace('₹', '').replace(',', '')) if price_tag else 0
                
                self.logger.info(f"Scraping product at page {page_number}...")
                details = self.scrape_product_details(product_link)
                if details:
                    details["product_price"] = product_price
                    scraped_data.append(details)
        self.data_storage.cache_data(page_number, scraped_data)
        self.logger.info(f"Scraped {len(scraped_data)} products from page {page_number}.")
        return scraped_data
