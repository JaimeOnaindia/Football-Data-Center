import logging
import os

from django.conf import settings
from django.core.management.base import BaseCommand
import pandas as pd

import requests
from bs4 import BeautifulSoup

from utils.command_decorator import command_decorator


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'
    USELESS_POSITIONS = ['MFFW', 'FWMF', 'DFMF', 'FWDF', 'MFDF', 'DFFW']
    log = logging.getLogger(__name__)

    @command_decorator(log, 'import_players_from_csv')
    def handle(self, *args, **options):
        self.main()

    def main(self):
        self.import_players_from_kaggle_csv()

    @staticmethod
    def import_players_from_kaggle_csv():
        filename_dir = os.path.join(settings.BASE_DIR, 'Players/Data/players_stats_21-22.csv')
        df_records = pd.read_csv(filename_dir, encoding='latin-1', sep=';')

        transfermarket_response = requests.get(
            settings.TRANSFERMARKET_SEARCH_RESULT_BY_PLAYER.format(player='messi'),
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        soup = BeautifulSoup(transfermarket_response.text, 'lxml')
        players_table_html = soup.table
        print(players_table_html)
        print("aa")


