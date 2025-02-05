# FastApiScraper
A Fast API based website scraper

# File Structure
```
FastApiScraper/
│
├── app.py                    # Main FastAPI application
├── config.py                 # Configuration file with constants and selectors
├── data_storage.py           # Handles storing and retrieving data from Redis, also stores to a JSON file
├── notifier.py               # Handles notification (email, logs, or any custom notification system)
├── scraper.py                # Scraper class responsible for scraping product details
├── utils.py                  # Utility functions like fetch_url, image download, and logging setup
├── requirements.txt          # Python dependencies required for the project
├── scraped_data.json         # JSON file for storing scraped product data
├── static/                   # Directory for storing downloaded product images
│   └── images/               # Folder for the images (will be created by the scraper)
├── README.md                 # Project documentation (this file)
```

# Install Dependencies
```
pip install -r requirements.txt`
```

# Setup Redis
```
brew install redis
redis-server
```

# Run the app
```
uvicorn main:app --reload`
```

# Example cURL
```
curl --location --request GET 'http://localhost:8000/scrape' \
--header 'Authorization: Bearer pass' \
--header 'Content-Type: application/json' \
--data '{
    "pages": 2,
    "proxy": "167.71.48.245:8080"
}'
```

# Sample Response
```
[
  {
    "product_title": "Example Product 1",
    "product_price": 100.0,
    "path_to_image": "static/images/example_product_1.jpg"
  },
  {
    "product_title": "Example Product 2",
    "product_price": 150.0,
    "path_to_image": "static/images/example_product_2.jpg"
  }
]
```
