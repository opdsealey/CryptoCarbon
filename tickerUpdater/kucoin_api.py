import zoneinfo
from datetime import timezone
from tickers.models import (
    Ticker,
    Market,
    LookupSchedule,
    LookupEvent,
    LookUpScheduleType,
    TradeKlines,
)
from django.db import IntegrityError
from django.utils import timezone as django_timezone
from django.utils.timezone import make_aware

import requests
import time
import datetime
from pprint import pprint

API_KEY = "61aa55749734ff0001494238"
API_SECRET = "9ae4f020-2896-4d4b-8fcb-7a5af4bc5651"
API_PASSPHRAASE = "4Ib!LiP5j7Xi%B@3Tu9Z&xsFXH#S0kwi"


HEADERS = {
    "Accept": "application/json",
    "User-Agent": "carbon",
    "Content-Type": "application/json",
    "KC-API-KEY": API_KEY,
    "KC-API-PASSPHRASE": API_PASSPHRAASE,
}


def get_tickers():
    start = time.time()
    print(
        f"Schedule started at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start))}"
    )
    for market in Market.objects.all():
        if market.name == "kucoin":
            url = "https://api.kucoin.com/api/v1/market/allTickers"

            r = requests.get(url, headers=HEADERS)
            created_tickers = 0
            for ticker in r.json()["data"]["ticker"]:
                obj, created = Ticker.objects.get_or_create(
                    market=market,
                    symbol=ticker["symbol"],
                    symbol_name=ticker["symbolName"],
                )

                if created:
                    created_tickers += 1

                daily_schedule = LookUpScheduleType.objects.get(value="1day")
                LookupSchedule.objects.get_or_create(
                    ticker=obj, schedule=daily_schedule
                )

        print(
            f"Created {created_tickers} tickers for market {market.name} - time taken {time.time() - start}"
        )


def daily_klines(count=15):
    """Get daily klines for stocks.

    Args:
        count (int): number of tickers to look up.
    """
    # Does all daily lookups
    daily_schedules = LookupSchedule.objects.filter(schedule__value="1day")
    for j, daily_schedule in enumerate(daily_schedules):
        if count is not None and j >= count:
            break

        events = LookupEvent.objects.filter(
            lookup_schedule=daily_schedule, complete=True
        ).order_by("-end")
        end = django_timezone.now()
        if events:
            # Is dif between previous event and now greater than the diff?
            if (events[0].end + datetime.timedelta(days=1)) >= end:
                continue
            else:
                start = events[0].end
        else:
            # 1500 is number of data points returned.
            start = end - datetime.timedelta(days=1500)
            # No previous events. Get them all.

        print(f"Getting daily Klines for {daily_schedule.ticker.symbol}")
        data = get_klines_for_symbol(
            daily_schedule.ticker.symbol,
            start=int(start.timestamp()),
            end=int(end.timestamp()),
            type=daily_schedule.schedule.value,
        )

        e = LookupEvent(lookup_schedule=daily_schedule)
        e.start = start
        e.end = end
        e.save()
        try:
            for i, datum in enumerate(data["data"]):
                start = datetime.datetime.fromtimestamp(int(datum[0]))
                end = start + datetime.timedelta(days=1)
                open = datum[1]
                close = datum[2]
                high = datum[3]
                low = datum[4]
                volume = datum[5]
                amount = datum[6]

                kine = TradeKlines(
                    ticker=daily_schedule.ticker,
                    start=make_aware(start, timezone=timezone.utc),
                    end=make_aware(end, timezone=timezone.utc),
                    open=open,
                    close=close,
                    high=high,
                    low=low,
                    volume=volume,
                    amount=amount,
                )
                try:
                    kine.save()
                except IntegrityError:
                    pass

            if e:
                e.datum_count = i
                e.complete = True
                e.save()
        except KeyError:
            print("Error - ")
            pprint(data)

    print(f"Finished getting daily klines. Got klines for {j} tickers.")


def get_klines_for_symbol(symbol, start, end, type="1min"):
    url = f"https://api.kucoin.com/api/v1/market/candles?type={type}&symbol={symbol}&startAt={start}&endAt={end}"
    r = requests.get(url, headers=HEADERS)
    return r.json()
