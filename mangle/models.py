from django.db import models
from model_utils.models import TimeStampedModel

from common.model_fields import CharFieldWithoutChoicesMigrations

from . import constants


class Instrument(TimeStampedModel):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=100, unique=True)
    isin = models.CharField(max_length=12, db_index=True, blank=True, default="")
    bloomberg_code = models.CharField(max_length=20)
    description = models.TextField(blank=True, default="")

    def __str__(self):
        return f"#{self.pk} {self.code}"


class InstrumentConfiguration(TimeStampedModel):
    instrument = models.OneToOneField(Instrument, on_delete=models.CASCADE)
    configuration = models.JSONField(blank=True, default=dict)
    price_synchronization_interval = CharFieldWithoutChoicesMigrations(
        max_length=20,
        choices=constants.IntervalChoices.choices,
        default=constants.IntervalChoices.DAILY,
    )
    stock_exchange = CharFieldWithoutChoicesMigrations(
        max_length=20,
        default="",
        choices=constants.StockExchangeChoices.choices,
    )

    timezone = CharFieldWithoutChoicesMigrations(
        max_length=50,
        choices=constants.TimeZoneChoices.choices,
        default=constants.TimeZoneChoices.AMERICA_NEW_YORK,
    )
    price_delay_threshold = CharFieldWithoutChoicesMigrations(
        max_length=20,
        choices=constants.IntervalChoices.choices,
        blank=True,
        default="",
    )
    yield_synchronization_interval = CharFieldWithoutChoicesMigrations(
        max_length=20,
        choices=constants.IntervalChoices.choices,
        default="",
    )
    yield_delay_threshold = CharFieldWithoutChoicesMigrations(
        max_length=20,
        choices=constants.IntervalChoices.choices,
        blank=True,
        default="",
    )
    price_source = CharFieldWithoutChoicesMigrations(
        max_length=20,
        choices=constants.ReportSourceChoices.choices,
        default="",
    )
    basic_metrics_source = CharFieldWithoutChoicesMigrations(
        max_length=20,
        blank=True,
        choices=constants.ReportSourceChoices.choices,
        default="",
    )

    def __str__(self):
        return f"{self.instrument} Configuration"


class PriceData(TimeStampedModel):
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=15, decimal_places=10)
    price_at = models.DateTimeField()

    def __str__(self):
        return f"{self.instrument} Price at {self.price_at}: {self.price}"


class LatestPriceData(TimeStampedModel):
    instrument = models.OneToOneField(Instrument, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=15, decimal_places=10)
    price_at = models.DateTimeField()

    def __str__(self):
        return f"{self.instrument} Latest Price at {self.price_at}: {self.price}"


class YieldReport(TimeStampedModel):
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)
    report_at = models.DateTimeField()

    def __str__(self):
        return f"{self.instrument} Yield Report for {self.report_at}"


class YieldData(TimeStampedModel):
    report = models.ForeignKey(YieldReport, on_delete=models.CASCADE)
    instrument = models.ForeignKey(
        Instrument,
        on_delete=models.CASCADE,
        db_comment="Duplication for speed",
    )
    yield_value = models.DecimalField(max_digits=10, decimal_places=5)
    yield_at = models.DateTimeField()
    yield_interval = models.CharField(
        max_length=20,
        choices=constants.YieldIntervalChoices.choices,
    )

    def __str__(self):
        return f"{self.instrument} Yield at {self.yield_at}: {self.yield_value}"
