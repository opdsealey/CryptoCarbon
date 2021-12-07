from django.core.management.base import BaseCommand, CommandError

from tickers.models import Market

MARKETS = ["kucoin"]


class Command(BaseCommand):
    help = "Adds arguments to the database"

    def handle(self, *args, **options):
        created_count = 0
        for market in MARKETS:
            _, c = Market.objects.get_or_create(name=market)
            if c:
                created_count += 1

        print(f"Added {created_count} markets.")
