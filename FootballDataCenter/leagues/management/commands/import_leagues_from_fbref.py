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

    @command_decorator(log, 'import_leagues_from_fbref')
    def handle(self, *args, **options):
        self.main()

    def main(self):
        table_id = 'compare_passing_types'
        url = settings.FBREF_5_EUROPEAN_LEAGUES_TEAMS_URL
        web_scrapper = WebScrapper(url=url, table_id=table_id)
        players_stats_df = web_scrapper.get_dataframe_from_web_table()
