import os

from dotenv import load_dotenv

from libs.scraper import Scraper
from libs.database import Database
from libs.logs import logger

load_dotenv()
VAR = os.getenv("VAR")


def main():

    scraper = Scraper()
    letters = [chr(i) for i in range(65, 91)]
    for letter in letters:
        scraper.set_letter(letter)
        max_pages = scraper.get_max_pages_num()
        
        for page in range(1, max_pages + 1):
            
            # Get data
            logger.info(f"Getting data from letter '{letter}' page '{page}'...")
            scraper.set_page(page)
            page_data = scraper.get_page_data()
            print(page_data)
    

if __name__ == "__main__":
    main()
