from django.db import models
from model_utils.models import TimeStampedModel

from common import constants
from common.model_fields import CharFieldWithoutChoicesMigrations


class Instrument(TimeStampedModel):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=100, unique=True)
    instrument_type = CharFieldWithoutChoicesMigrations(
        max_length=20,
        choices=constants.InstrumentTypeChoices.choices,
        default=constants.InstrumentTypeChoices.STOCK,
        blank=True,
    )
    isin = models.CharField(max_length=12, db_index=True, blank=True, default="")
    bloomberg_code = models.CharField(max_length=20, blank=True, default="")
    description = models.TextField(blank=True, default="")

    def __str__(self):
        return f"#{self.pk} {self.code}"


class PriceData(TimeStampedModel):
    """Represents historical price data for an instrument.
    NAV data for funds is also stored here."""

    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=15, decimal_places=10)
    price_at = models.DateTimeField(db_index=True)

    def __str__(self):
        return f"{self.instrument} Price at {self.price_at}: {self.price}"


class LatestPriceData(TimeStampedModel):
    instrument = models.OneToOneField(Instrument, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=15, decimal_places=10)
    price_at = models.DateTimeField()

    def __str__(self):
        return f"{self.instrument} Latest Price at {self.price_at}: {self.price}"


class Report(TimeStampedModel):
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)
    report_type = CharFieldWithoutChoicesMigrations(
        max_length=20,
        choices=constants.ReportTypeChoices.choices,
        default="",
        blank=True,
    )
    report_at = models.DateTimeField(db_index=True)
    published_at = models.DateTimeField(db_index=True)

    def __str__(self):
        return f"{self.instrument} Report {self.report_type} at {self.published_at}"


class LatestReport(TimeStampedModel):
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)
    report_type = CharFieldWithoutChoicesMigrations(
        max_length=20,
        choices=constants.ReportTypeChoices.choices,
        default="",
        blank=True,
    )
    report = models.OneToOneField(Report, on_delete=models.CASCADE)
    report_at = models.DateTimeField()
    published_at = models.DateTimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["instrument", "report_type"],
                name="unique_instrument_report_type",
            ),
        ]

    def __str__(self):
        return f"{self.instrument} Latest Report {self.report_type} at {self.published_at}"


class ReportData(TimeStampedModel):
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    key_value = models.CharField(max_length=255)
    value_number = models.DecimalField(max_digits=30, decimal_places=10, null=True, blank=True)
    value_text = models.TextField(default="", blank=True)

    def __str__(self):
        return f"{self.report} Data {self.key_value}: {self.value_number or self.value_text}"
