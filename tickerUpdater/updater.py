from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

from tickerUpdater import kucoin_api
from tickerUpdater import analysis


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(kucoin_api.get_tickers, "interval", days=1)
    scheduler.add_job(kucoin_api.daily_klines, "interval", minutes=10)
    scheduler.add_job(analysis.calculate_average_true_return, "interval", hours=12)
    scheduler.start()
