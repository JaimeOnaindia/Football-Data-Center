import logging
from itertools import groupby

from django.conf import settings
from django.core.management.base import BaseCommand
import pandas as pd
from pandas import DataFrame

from geo.models import Country
from players.models import BasePlayer, BasePlayerStatsFBREF
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

    def process_stats_dataframe(self, players_stats_df: DataFrame) -> DataFrame:
        player_playing_time_stats_df = self.get_playing_time_dataframe(players_stats_df)
        player_performance_stats_df = self.get_performance_dataframe(players_stats_df)
        player_expected_stats_df = self.get_expected_dataframe(players_stats_df)
        player_progression_stats_df = self.get_progression_dataframe(players_stats_df)

        if self.dataframes_has_same_shape(
                player_playing_time_stats_df,
                player_performance_stats_df,
                player_expected_stats_df,
                player_progression_stats_df
        ):
            players_full_dataframe = pd.concat(
                [player_playing_time_stats_df,
                 player_performance_stats_df,
                 player_expected_stats_df,
                 player_progression_stats_df], axis=1
            ).fillna(0)

            players_full_dataframe = players_full_dataframe[
                players_full_dataframe['name'] != 'Player'
            ]
            players_full_dataframe['position'] = players_full_dataframe['position'].apply(
                self.process_players_positions
            )
            return players_full_dataframe

    @staticmethod
    def dataframes_has_same_shape(*args):
        shape_list = [data_frame.shape[0] for data_frame in args]
        g = groupby(shape_list)
        return next(g, True) and not next(g, False)

    @staticmethod
    def get_playing_time_dataframe(players_stats_df: DataFrame) -> DataFrame:
        columns = settings.FBREF_PLAYERS_BASIC_INFO
        player_playing_time_stats_df = players_stats_df[0].iloc[:, :11]
        player_playing_time_stats_df.columns = columns[:11]
        return player_playing_time_stats_df

    @staticmethod
    def get_performance_dataframe(players_stats_df: DataFrame) -> DataFrame:
        columns = settings.FBREF_PLAYERS_PERFORMANCE
        player_performance_stats_df = players_stats_df[0]['Performance']
        player_performance_stats_df.columns = columns
        return player_performance_stats_df

    @staticmethod
    def get_expected_dataframe(players_stats_df: DataFrame) -> DataFrame:
        columns = settings.FBREF_PLAYERS_EXPECTED
        player_expected_df = players_stats_df[0]['Expected']
        player_expected_df.columns = columns
        return player_expected_df

    @staticmethod
    def get_progression_dataframe(players_stats_df: DataFrame) -> DataFrame:
        columns = settings.FBREF_PLAYERS_PROGRESSION
        player_progression_df = players_stats_df[0]['Progression']
        player_progression_df.columns = columns
        return player_progression_df

    @staticmethod
    def process_players_positions(position: str) -> str:
        positions_dict = {
            'GK': 'GK',
            'DF': 'DF',
            'DF,FW': 'RB',
            'FW,DF': 'LB',
            'MF,DF': 'DF,MF',
            'DF,MF': 'DF,MF',
            'MF': 'MF',
            'FW,MF': 'CAM',
            'MF,FW': 'RW',
            'FW': 'FW'
        }
        return positions_dict.get(position)

    def update_or_create_players_to_database(
            self, players_processed_df: DataFrame
    ):
        for row in players_processed_df.to_dict('records'):
            code_alpha_3 = row['nation'].split(' ')[-1] if row['nation'] != 0 else None
            country = Country.objects.filter(code_alpha_3=code_alpha_3).first()
            base_players_defaults = {'team_name': row['team'], 'country': country}
            BasePlayer.objects.update_or_create(
                name=row['name'],
                defaults=base_players_defaults
            )
            fbref_players_defaults = self.build_defaults_fields(row)
            BasePlayerStatsFBREF.objects.update_or_create(
                name=row['name'],
                defaults=fbref_players_defaults
            )

    @staticmethod
    def build_defaults_fields(row):
        fbref_players_defaults = {
            'original_position': row['position'],
            'matches_played': row['matches_played'],
            'as_starter': row['starter'],
            'minutes_played': row['minutes_played'],
            'team_name': row['team'],
            'goals': row['goals'],
            'assists': row['assists'],
            'non_pen_goals': row['non_pen_goals'],
            'penalty_goals': row['penalty_goals'],
            'penalty_attempts': row['penalty_attempts'],
            'yellow_cards': row['yellow_cards'],
            'red_cards': row['red_cards'],
            'exp_goals': row['exp_goals'],
            'exp_non_pen_goals': row['exp_non_pen_goals'],
            'exp_goals_assists': row['exp_goals_assists'],
            'expected_non_pen_goals_assists': row['expected_non_pen_goals_assists'],
            'progressive_carries': row['progressive_carries'],
            'progressive_passes': row['progressive_passes'],
            'progressive_passes_received': row['progressive_passes_received']
        }
        return fbref_players_defaults
