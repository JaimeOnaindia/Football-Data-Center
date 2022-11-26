import pandas as pd
import requests
from bs4 import BeautifulSoup


class WebScrapper:
    def __init__(self, url, table_id=None):
        self.url = url
        self.table_id = table_id

    def get_dataframe_from_web_table(self):
        fbref_response = requests.get(url=self.url)
        soup = BeautifulSoup(fbref_response.text, 'lxml')
        table_prettified = soup.table.prettify()
        table_dataframe = pd.read_html(table_prettified)
        return table_dataframe
