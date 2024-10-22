from time import sleep

import bs4
import requests


class Scraper():
    
    def __init__(self):
        """ Load initial data and selectors """
        
        self.home_page = "https://medicamentosplm.com/Home/Medicamento"
        self.data = []
        self.selectors = {
            "page_btn": '.row + .container li.page-item',
        }
        
    def __get_page_soup__(self, page: int) -> bs4.BeautifulSoup:
        """ Return bs4 instance of a specific page
        
        Args:
            page (int): The page number
        
        Returns:
            bs4.BeautifulSoup: The page content
        """
        
        url = f"{self.home_page}/A/{page}"
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
        sleep(2)
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
    
    def __get_page_data__(self) -> dict:
        pass
        
    def get_data(self):
        
        max_pages = self.__get_max_pages_num__()
        print(max_pages)