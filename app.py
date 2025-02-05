from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel, conint
from scraper import Scraper
from data_storage import DataStorage
from notifier import Notifier
import logging

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ScrapeRequest(BaseModel):
    pages: conint(ge=1) # to accept only positive integers
    proxy: str = None # Optional 

scraper = Scraper()
data_storage = DataStorage()
notifier = Notifier()

SECRET_TOKEN = "pass"
def token_auth(authorization: str = Header(None)):
    """ Function to extract and validate token """
    if authorization is None or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization header missing or incorrect format")
    
    token = authorization[len("Bearer "):]
    
    if token != SECRET_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    return token


@app.get("/scrape")
async def scrape(request: ScrapeRequest, token: str = Depends(token_auth)):
    try:
        all_data = []
        for page in range(1, request.pages + 1):
            logger.info(f"Starting to scrape page {page}...")
            page_data = scraper.scrape_page(page)
            all_data.extend(page_data)

        data_storage.update_data(all_data)

        message = f"Scraping complete. Total products scraped and updated: {len(all_data)}"
        notifier.notify(message)
        
        return {"message": message, "data": all_data}

    except Exception as e:
        logger.error(f"Error during scraping: {e}")
        raise HTTPException(status_code=500, detail="An error occurred during scraping")
