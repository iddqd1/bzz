from typing import Any

from django.db import models
from django.utils import timezone
from model_utils.models import TimeStampedModel

from common import constants
from common.model_fields import CharFieldWithoutChoicesMigrations


class InstrumentConfiguration(TimeStampedModel):
    instrument = models.OneToOneField("mangle.Instrument", on_delete=models.CASCADE)
    auto_approve = models.BooleanField(default=True)
    price_synchronization_interval = CharFieldWithoutChoicesMigrations(
        max_length=20,
        choices=constants.IntervalChoices.choices,
        default="",
        blank=True,
    )
    stock_exchange = CharFieldWithoutChoicesMigrations(
        max_length=20,
        default="",
        choices=constants.StockExchangeChoices.choices,
        blank=True,
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
        blank=True,
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
        blank=True,
    )
    basic_metrics_source = CharFieldWithoutChoicesMigrations(
        max_length=20,
        blank=True,
        choices=constants.ReportSourceChoices.choices,
        default="",
    )

    def __str__(self):
        return f"{self.instrument} Configuration"


class ReportType(TimeStampedModel):
    id = CharFieldWithoutChoicesMigrations(
        max_length=20,
        choices=constants.ReportTypeChoices.choices,
        primary_key=True,
    )

    def __str__(self):
        return f"{self.pk} report type"


class WebPageScraperConfiguration(TimeStampedModel):
    instrument_configuration = models.ForeignKey(
        InstrumentConfiguration,
        on_delete=models.CASCADE,
    )
    url = models.URLField(unique=False)
    is_active = models.BooleanField(default=True)
    last_scraped_at = models.DateTimeField(null=True, blank=True)
    custom_query = models.TextField(
        blank=True,
        default="",
        help_text="Custom query to extract data from the webpage.",
    )
    report_types = models.ManyToManyField(ReportType)
    active = models.BooleanField(default=True)
    version = models.IntegerField(default=1)

    def __str__(self):
        return f"#{self.pk} WebPageScraperConfiguration for {self.url}"


class ScrapedData(TimeStampedModel):
    approved = models.BooleanField(default=False)
    approved_at = models.DateTimeField(null=True, blank=True, db_index=True)
    instrument_configuration = models.ForeignKey(
        InstrumentConfiguration,
        on_delete=models.CASCADE,
        db_comment="The instrument configuration associated with the scraped data.",
    )
    source_type = CharFieldWithoutChoicesMigrations(
        max_length=20,
        choices=constants.ReportSourceChoices.choices,
        default="",
        blank=True,
    )
    data_hash = models.CharField(max_length=64, unique=True, null=True)  # noqa: DJ001
    report_type = models.ForeignKey(ReportType, on_delete=models.CASCADE)
    data = models.JSONField(help_text="The scraped data in JSON format.", db_comment="Scraped data in JSON format")
    raw_data = models.TextField(blank=True, default="", db_comment="Raw scraped data as text. Optional")

    def __str__(self):
        return f"#{self.pk} RawReport for {self.instrument_configuration.instrument}"

    def save(self, *args: Any, **kwargs: Any) -> None:
        if self.approved and not self.approved_at:
            self.approved_at = timezone.now()
        return super().save(*args, **kwargs)
