import datetime
import logging

from django.conf import settings
from django.core.management.base import BaseCommand
import pandas as pd

from geo.models import Country
from players.models import BasePlayer
from utils.command_decorator import command_decorator
from utils.web_scrapper import WebScrapper


class Command(BaseCommand):
    log = logging.getLogger(__name__)

    @command_decorator(log, 'import_players_from_fbref')
    def handle(self, *args, **options):
        self.main()

    def main(self):
        url = settings.FBREF_5_EUROPEAN_LEAGUES_PLAYERS_URL
        web_scrapper = WebScrapper(url)
        players_stats_df = web_scrapper.get_dataframe_from_web_table()
        players_processed_df = self.process_stats_dataframe(players_stats_df)
        self.update_or_create_players_to_database(players_processed_df)

    def process_stats_dataframe(self, players_stats_df):
        columns = settings.FBREF_5_EUROPEAN_LEAGUES_PLAYERS_COLUMNS
        player_playing_time_stats_df = players_stats_df[0].iloc[:, :11]
        player_playing_time_stats_df.columns = columns[:11]
        player_performance_stats_df = players_stats_df[0]['Performance']
        player_expected_stats_df = players_stats_df[0]['Expected']
        players_full_dataframe = pd.concat(
            [player_playing_time_stats_df,
             player_performance_stats_df,
             player_expected_stats_df], axis=1, ignore_index=True
        ).fillna(0)
        players_full_dataframe = players_full_dataframe[
            players_full_dataframe[1] != 'Player'
        ]
        players_full_dataframe.columns = settings.FBREF_5_EUROPEAN_LEAGUES_PLAYERS_COLUMNS
        players_full_dataframe = players_full_dataframe.apply(
            self.create_datetime_player_birth, axis=1
        )
        return players_full_dataframe

    @staticmethod
    def create_datetime_player_birth(row):
        valid_year_and_age_format = row.born_year != 0 and row.age != 0
        if valid_year_and_age_format:
            born_year = int(row.born_year)
            age = int(row.age[:-4])
            row['date_birth'] = (datetime.date(born_year, 1, 1)
                                 + datetime.timedelta(days=age))
        else:
            row['date_birth'] = None
        return row

    @staticmethod
    def update_or_create_players_to_database(players_processed_df):
        for row in players_processed_df.to_dict('records'):
            code_alpha_3 = row['nation'].split(' ')[-1] if row['nation'] != 0 else None
            country = Country.objects.filter(code_alpha_3=code_alpha_3).first()
            base_players_default = {'team_name': row['team']}

            BasePlayer.objects.update_or_create(
                name=row['name'],
                date_birth=row['date_birth'],
                country=country,
                defaults=base_players_default
            )
