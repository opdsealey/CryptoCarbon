from django.core.management.base import BaseCommand, CommandError
import time
from analysis.methods import average_true_range
from tickers.models import Ticker, TradeKlines, Market
from statistics import mean


class Command(BaseCommand):
    help = """Calculates the average true range (https://www.investopedia.com/ask/answers/021015/what-best-measure-given-stocks-volatility.asp) 
            for a ticker for each day over aa 14 day period."""

    def add_arguments(self, parser):
        parser.add_argument("symbol", type=str)
        parser.add_argument(
            "--update", dest="update", default=False, action="store_true"
        )

    def handle(self, *args, **options):
        if options["symbol"] == "all":
            print("Updating ATR for all klines, this may take some time...")
            s = time.time()
            run_times = []
            for market in Market.objects.prefetch_related("ticker_set").all():
                for ticker in market.ticker_set.all():
                    t2 = time.time()
                    average_true_range(ticker, set_values=True)
                    run_times.append(time.time() - t2)

            print(f"Time taken: {time.time()- s}s - avg ATR time: {mean(run_times)}s")

        else:
            try:
                ticker = Ticker.objects.get(symbol=options["symbol"])
            except Ticker.DoesNotExist:
                raise CommandError(
                    f"No ticker with symbol: {options['symbol']} exists."
                )

            atr = average_true_range(ticker)

            print(atr)
