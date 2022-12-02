import logging
import os

import pandas as pd
from django.conf import settings
from django.core.management import BaseCommand

from geo.models import Country
from utils.command_decorator import command_decorator


class Command(BaseCommand):
    log = logging.getLogger(__name__)

    @command_decorator(log, 'import_countries')
    def handle(self, *args, **options):
        self.main()

    def main(self):
        filename_dir = os.path.join(settings.BASE_DIR, 'geo/data/country-information.csv')
        countries_df = pd.read_csv(filename_dir, encoding='utf-8', sep=',')
        self.update_countries_to_database(countries_df)

    @staticmethod
    def update_countries_to_database(countries_df):
        for country in countries_df.to_dict('records'):
            defaults = {'name': country['name'],
                        'code_alpha_2': country['alpha-2'],
                        'region': country['region'],
                        'sub_region': country['sub-region']}
            Country.objects.update_or_create(
                code_alpha_3=country['alpha-3'],
                defaults=defaults
            )
