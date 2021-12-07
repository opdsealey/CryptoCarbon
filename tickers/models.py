from typing import Sequence
from django.db import models

# Create your models here.
class Market(models.Model):
    name = models.CharField(max_length=256, null=False)


class Ticker(models.Model):
    symbol = models.CharField(max_length=24)
    symbol_name = models.CharField(max_length=24)

    market = models.ForeignKey(Market, on_delete=models.CASCADE)


class LookUpScheduleType(models.Model):
    value = models.CharField(max_length=6)


class TradeKlines(models.Model):
    ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE)

    start = models.DateTimeField()
    end = models.DateTimeField()

    # Filled Price
    open = models.FloatField()
    close = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    volume = models.FloatField()
    amount = models.FloatField()

    atr = models.FloatField(null=True, blank=True, default=None)

    class Meta:
        unique_together = ("ticker", "start", "end")


class LookupSchedule(models.Model):
    schedule = models.ForeignKey(LookUpScheduleType, on_delete=models.CASCADE)
    ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("schedule", "ticker")


class LookupEvent(models.Model):
    complete = models.BooleanField(default=False)
    lookup_schedule = models.ForeignKey(LookupSchedule, on_delete=models.CASCADE)
    # Start is the oldder date.
    start = models.DateTimeField()
    end = models.DateTimeField()
    datum_count = models.IntegerField(default=0)
