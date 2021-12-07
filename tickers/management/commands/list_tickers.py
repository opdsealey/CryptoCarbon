from django.core.management.base import BaseCommand, CommandError

from tickers.models import Market, Ticker


class Command(BaseCommand):
    help = "Lists all tickers currently in the database"

    def handle(self, *args, **options):
        for i, ticker in enumerate(Ticker.objects.all()):
            print(f"[{str(i).zfill(4)}]\t{ticker.symbol}\t{ticker.market.name}")

        print(f"\n\nTotal: {i}")
