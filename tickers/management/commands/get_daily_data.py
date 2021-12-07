from django.core.management.base import BaseCommand, CommandError

from tickerUpdater.kucoin_api import daily_data


class Command(BaseCommand):
    help = "Performs all daily updates"

    def handle(self, *args, **options):
        daily_data()
