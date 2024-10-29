import bs4
import requests
from time import sleep

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
                "medication": {
                    "value": '> div:nth-child(1)',
                    "type": str,
                },
                "substance": {
                    "value": '> div:nth-child(2) > a',
                    "type": list,
                },
                "pharmaceutical_form": {
                    "value": '> div:nth-child(3)',
                    "type": str,
                },
                "laboratory": {
                    "value": '> div:nth-child(4)',
                    "type": str,
                },
                "presentation": {
                    "value": '> div:nth-child(5)',
                    "type": str,
                },
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
        
    def get_max_pages_num(self) -> int:
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
    
    def get_page_data(self) -> list[dict]:
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
        for row_index in range(1, len(rows)):
            
            # Scrape row data
            row_data = {}
            selector_row = self.selectors["table_row"]
            table_columns_selecrtors = self.selectors["table_columns"]
            for selector_name, selector_data in table_columns_selecrtors.items():
                
                selector_value = selector_data["value"]
                selector_type = selector_data["type"]
                
                # Get value
                selector_row = f"{selector_row}:nth-child({row_index + 1})"
                selector_row_value = f"{selector_row} {selector_value}"
                values_elems = soup.select(selector_row_value)
                values = list(map(
                    lambda value: value.text.replace(",", "").strip(),
                    values_elems
                ))
                
                if selector_type == str:
                    values = values[0]
                    for char in ["\n", "\t", "\r"]:
                        values = values.replace(char, "")
                  
                # Clean and save value
                row_data[selector_name] = values
        
            # Save row data
            data.append(row_data)
            
        return data
    
    def set_letter(self, letter: str):
        """ Set the letter to scrape
        
        Args:
            letter (str): The letter to scrape
        """
        
        self.letter = letter
        
    def set_page(self, page: int):
        """ Set the page to scrape
        
        Args:
            page (int): The page to scrape
        """
        
        self.page = page