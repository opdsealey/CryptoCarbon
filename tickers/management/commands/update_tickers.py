from django.core.management.base import BaseCommand, CommandError

from tickerUpdater.kucoin_api import get_tickers


class Command(BaseCommand):
    help = "Updates tickers."

    def handle(self, *args, **options):
        get_tickers()
