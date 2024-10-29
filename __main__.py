import os
import time

from dotenv import load_dotenv

from libs.scraper import Scraper
from libs.database import Database
from libs.logs import logger

load_dotenv()
MONGODB_USER = os.getenv("MONGODB_USER")
MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD")
MONGODB_HOST = os.getenv("MONGODB_HOST")
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE")
MONGODB_COLLECTION = os.getenv("MONGODB_COLLECTION")


def main():
    
    # Calculate start time
    start_time = time.time()

    # Start instances
    scraper = Scraper()
    database = Database(
        MONGODB_USER,
        MONGODB_PASSWORD,
        MONGODB_HOST,
        MONGODB_DATABASE,
        MONGODB_COLLECTION
    )
    
    # Delete old data
    database.delete_collection()
    
    letters = [chr(i) for i in range(65, 91)]
    for letter in letters:
        scraper.set_letter(letter)
        max_pages = scraper.get_max_pages_num()
        
        for page in range(1, max_pages + 1):
            
            # Get data
            logger.info(f"Getting data from letter '{letter}' page '{page}'...")
            scraper.set_page(page)
            page_data = scraper.get_page_data()
            
            # Save page data in mongo
            database.insert_data(page_data)
            
        end_time = time.time()
        total_time = end_time - start_time
        total_time_minutes = total_time / 60
        total_time_hours = total_time / 3600
        logger.debug(f"Total time: {total_time:.2f} seconds")
        logger.debug(f"Total time: {total_time_minutes:.2f} minutes")
        logger.debug(f"Total time: {total_time_hours:.2f} hours")
    

if __name__ == "__main__":
    main()
