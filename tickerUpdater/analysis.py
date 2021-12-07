from analysis.methods import average_true_range
from tickers.models import Market, Ticker


def calculate_average_true_return():
    for market in Market.objects.prefetch_related("ticker_set").all():
        for ticker in market.ticker_set.all:
            average_true_range(ticker, set_values=True)

    print(f"Finished updating ATR.")
