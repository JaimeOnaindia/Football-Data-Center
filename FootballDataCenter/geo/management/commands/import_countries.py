import logging

from django.core.management import BaseCommand

from utils.command_decorator import command_decorator


class Command(BaseCommand):
    log = logging.getLogger(__name__)

    @command_decorator(log, 'import_countries')
    def handle(self, *args, **options):
        self.main()

    def main(self):
        pass
