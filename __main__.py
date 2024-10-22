import os
from dotenv import load_dotenv
from libs.scraper import Scraper

load_dotenv()
VAR = os.getenv("VAR")


def main():

    scraper = Scraper()
    data = scraper.get_data()


if __name__ == "__main__":
    main()
