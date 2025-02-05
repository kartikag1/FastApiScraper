import os
import json
import redis
import logging

cache = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

class DataStorage:
    def __init__(self, file_path='scraped_data.json', use_cache=True):
        self.file_path = file_path
        self.use_cache = use_cache

    def get_cached_data(self, key):
        if not self.use_cache:
            return None
        
        logging.info(f"Attempting to fetch cached data for {key}")
        cached_data = cache.get(key)
        if cached_data:
            logging.info(f"Cache hit for {key}")
            try:
                cached_data = json.loads(cached_data)
            except json.JSONDecodeError:
                logging.error(f"Error decoding cache for {key}.")
                return None
            return cached_data
        logging.info(f"Cache miss for {key}")
        return None

    def cache_data(self, key, data, expiration=3600):
        if not self.use_cache:
            return
        
        logging.info(f"Caching data for {key}. Data preview: {data[:3]}...")  # Preview first 3 items for debugging
        try:
            result = cache.set(key, json.dumps(data), ex=expiration)  # Cache for 1 hour
            if result:
                logging.info(f"Successfully cached data for {key}")
            else:
                logging.error(f"Failed to cache data for {key}")
        except Exception as e:
            logging.error(f"Error caching data for {key}: {e}")

    def load_data(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                return json.load(file)
        return []

    def save_data(self, data):
        with open(self.file_path, 'w') as file:
            json.dump(data, file, indent=4)

    def update_data(self, new_data):
        existing_data = self.load_data()
        
        for new_product in new_data:
            existing_product = next((p for p in existing_data if p['product_title'] == new_product['product_title']), None)
            if existing_product:
                if existing_product['product_price'] != new_product['product_price']:
                    existing_product.update(new_product)
            else:
                existing_data.append(new_product)
        
        self.save_data(existing_data)
