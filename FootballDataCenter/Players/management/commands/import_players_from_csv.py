from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
import pandas as pd

import requests
from bs4 import BeautifulSoup


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'
    USELESS_POSITIONS = ['MFFW', 'FWMF', 'DFMF', 'FWDF', 'MFDF', 'DFFW']

    def handle(self, *args, **options):
        self.main()

    def main(self):
        self.import_players_from_kaggle_csv()

    @staticmethod
    def import_players_from_kaggle_csv():
        df_records = pd.read_csv("C:/Users/Jaime/Documents/Jaime/PlayerStats2022.csv",
                                 encoding='latin-1',
                                 sep=';')
        transfermarket_response = requests.get(
            settings.TRANSFERMARKET_SEARCH_RESULT_BY_PLAYER.format(player='messi'),
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        soup = BeautifulSoup(transfermarket_response.text, 'lxml')
        players_table_html = soup.table
        print(players_table_html)
        print("aa")
