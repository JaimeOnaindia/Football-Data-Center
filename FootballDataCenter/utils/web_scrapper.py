import pandas as pd
import requests
from bs4 import BeautifulSoup


class WebScrapper:
    def __init__(self, url: str, table_id: str = None):
        self.url = url
        self.table_id = table_id

    def get_dataframe_from_web_table(self):
        fbref_response = requests.get(url=self.url)
        soup = BeautifulSoup(fbref_response.text, 'lxml')
        table_prettified = soup.table.prettify()
        table_dataframe = pd.read_html(table_prettified)
        if self.table_id:
            table_dataframe = pd.read_html(table_prettified, attrs={'id': self.table_id})
        return table_dataframe
