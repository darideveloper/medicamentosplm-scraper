from time import sleep

import bs4
import requests

from libs.logs import logger


class Scraper():
    
    def __init__(self):
        """ Load initial data and selectors """
        
        logger.info("Initializing Scraper...")
        self.home_page = "https://medicamentosplm.com/Home/Medicamento"
        self.data = []
        self.selectors = {
            "page_btn": '.row + .container li.page-item',
            "table_row": '.fila',
            "table_columns": {
                "medication": 'div:nth-child(1)',
                "substance": 'div:nth-child(2)',
                "pharmaceutical_form": 'div:nth-child(3)',
                "laboratory": 'div:nth-child(4)',
                "presentation": 'div:nth-child(5)',
            }
        }
        
        # Scraping control variables
        self.letter = ''
        self.page = 0
        
    def __get_page_soup__(self, page: int = 0) -> bs4.BeautifulSoup:
        """ Return bs4 instance of a specific page
        
        Returns:
            bs4.BeautifulSoup: The page content
        """
        
        if not page:
            page = self.page
        
        url = f"{self.home_page}/{self.letter}/{page}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'DNT': '1',
            'Cache-Control': 'max-age=0',
            
        }
        res = requests.get(url, headers=headers)
        html = res.text
        soup = bs4.BeautifulSoup(html, 'html.parser')
        sleep(5)
        return soup
        
    def __get_max_pages_num__(self) -> int:
        """ Return the max number resuluts pages

        Returns:
            int: The max number of pages
        """
        
        # Load first page and get soup
        soup = self.__get_page_soup__(1)
        
        # Get number of pages (remove next and previous buttons)
        page_btns = soup.select(self.selectors["page_btn"])
        pages = len(page_btns) - 2
        return pages
    
    def __get_page_data__(self) -> list[dict]:
        """ Get data from a specific page of results

        Returns:
            list[dict]: The data table's page
                medication: str
                substance: str
                pharmaceutical_form: str
                laboratory: str
                presentation: str
        """
        
        # Get page soup
        soup = self.__get_page_soup__()
        
        # Loop table rows (skip header)
        data = []
        rows = soup.select(self.selectors["table_row"])
        for row in rows[1:]:
            
            # Scrape row data
            row_data = {}
            table_columns_selecrtors = self.selectors["table_columns"]
            for selector_name, selector_value in table_columns_selecrtors.items():
                row_data[selector_name] = row.select_one(selector_value).text.strip()
                
            # Save row data
            data.append(row_data)
            
        return data
                
    def get_data(self):
        
        letters = [chr(i) for i in range(65, 91)]
        for letter in letters:
            self.letter = letter
            max_pages = self.__get_max_pages_num__()
            
            for page in range(1, max_pages + 1):
                
                # Get data
                logger.info(f"Getting data from letter '{letter}' page '{page}'...")
                self.page = page
                page_data = self.__get_page_data__()
                
                # Temp save data in csv
                import csv
                import os
                
                parent_folder = os.path.dirname(os.path.abspath(__file__))
                current_folder = os.path.dirname(parent_folder)
                csv_file = os.path.join(current_folder, "temp.csv")
                with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
                    writer = csv.DictWriter(file, fieldnames=page_data[0].keys())
                    for row in page_data:
                        writer.writerow(row)