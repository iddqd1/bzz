from django.contrib import admin

from . import models


@admin.register(models.InstrumentConfiguration)
class InstrumentConfigurationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "instrument",
        "price_synchronization_interval",
        "stock_exchange",
        "timezone",
        "price_delay_threshold",
        "yield_synchronization_interval",
        "yield_delay_threshold",
        "price_source",
        "basic_metrics_source",
    )
    search_fields = ("instrument__name", "instrument__code", "instrument__isin")
    list_filter = ("stock_exchange", "timezone")
    autocomplete_fields = ("instrument",)


@admin.register(models.WebPageScraperConfiguration)
class WebPageScraperConfigurationAdmin(admin.ModelAdmin):
    list_display = ("id", "url", "is_active", "last_scraped_at", "active")
    search_fields = ("url",)
    list_filter = ("is_active", "active")
    ordering = ("-last_scraped_at",)
    autocomplete_fields = ("instrument_configuration",)


@admin.register(models.ScrapedData)
class ScrapedDataAdmin(admin.ModelAdmin):
    list_display = ("id", "instrument", "data_type", "data_value", "scraped_at")
    search_fields = ("instrument__name", "instrument__code", "data_type")
    list_filter = ("data_type",)
    ordering = ("-scraped_at",)
