import logging
import os

from django.conf import settings
from django.core.management.base import BaseCommand
import pandas as pd

import requests
from bs4 import BeautifulSoup

from Players.models import Player
from utils.command_decorator import command_decorator


class Command(BaseCommand):
    log = logging.getLogger(__name__)

    @command_decorator(log, 'import_players_from_csv')
    def handle(self, *args, **options):
        self.main()

    def main(self):
        self.get_full_stats_dataframe()

    def get_full_stats_dataframe(self):
        players_stats_df = self.get_beautiful_soup()
        players_processed_df = self.process_stats_dataframe(players_stats_df)
        print("aa")

    @staticmethod
    def get_beautiful_soup():
        url = settings.FBREF_5_EUROPEAN_LEAGUES_PLAYERS_URL
        fbref_response = requests.get(url=url)
        soup = BeautifulSoup(fbref_response.text, 'lxml')
        players_table_byte = soup.table.prettify()
        players_stats = pd.read_html(players_table_byte)
        return players_stats

    def process_stats_dataframe(self, players_stats_df):
        player_playing_time_stats_df = self.select_first_n_columns(players_stats_df[0], 11)
        player_playing_time_stats_df.columns = settings.FBREF_5_EUROPEAN_LEAGUES_PLAYERS_COLUMNS
        player_performance_stats_df = players_stats_df[0]['Performance'].assign(
            id=player_playing_time_stats_df['id']
        )
        player_expected_stats_df = players_stats_df[0]['Expected'].assign(
            id=player_playing_time_stats_df['id']
        )
        players_full_dataframe = player_playing_time_stats_df.merge(
            player_playing_time_stats_df, how='left', on='id'
        )

    @staticmethod
    def select_first_n_columns(dataframe, number):
        new_dataframe = dataframe.iloc[:, :number]
        return new_dataframe

    @staticmethod
    def update_or_create_players_to_database(player_playing_time_stats_df):
        for row in player_playing_time_stats_df.to_dict('orient'):
            Player.objects.update_or_create(

            )
