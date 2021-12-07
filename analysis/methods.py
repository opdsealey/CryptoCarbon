import datetime
from typing import Optional
from functools import reduce
import pandas as pd
from pprint import pprint
from datetime import timedelta
import numpy as np
from tickers.models import TradeKlines, Ticker


def average_true_range(ticker: Ticker, set_values=False) -> Optional[pd.DataFrame]:
    """https://www.investopedia.com/ask/answers/021015/what-best-measure-given-stocks-volatility.asp

    Args:
        ticker (Ticker): [description]
        set_values (boolean): Write values to the database
    """
    klines = TradeKlines.objects.filter(ticker=ticker).order_by("-end").all().values()
    if not klines:
        return None

    data = pd.DataFrame(klines)

    # Trim data so that we have 15 more rows than the min value without an ATR, might be able to do this in SQL
    df = data.loc[data["atr"].isnull()]
    start_date = df["end"].min() - timedelta(days=15)
    mask = df["end"] > start_date
    data = df.loc[mask]

    data.set_index("end", inplace=True)

    if data.empty:
        return None

    high_low = data["high"] - data["low"]
    high_cp = np.abs(data["high"] - data["close"].shift())
    low_cp = np.abs(data["low"] - data["close"].shift())

    df = pd.concat([high_low, high_cp, low_cp], axis=1)
    true_range = np.max(df, axis=1)

    data["atr"] = true_range.rolling(14).mean()
    if set_values:
        objs = []
        for index, row in data.iterrows():
            if pd.isnull(row["atr"]):
                continue
            kline = TradeKlines.objects.get(pk=row["id"])
            if kline.atr is None:
                kline.atr = row["atr"]
                objs.append(kline)

        TradeKlines.objects.bulk_update(objs, ["atr"])

    return data
