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
    list_display = ("id", "url", "is_active", "created", "active")
    search_fields = ("url", "instrument_configuration__instrument__name", "instrument_configuration__instrument__code")
    list_filter = ("is_active", "active")
    ordering = ("-id",)
    autocomplete_fields = ("instrument_configuration",)


@admin.register(models.ScraperType)
class ScraperTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "created")
    search_fields = ("id",)
    ordering = ("-created",)


@admin.register(models.ScrapedData)
class ScrapedDataAdmin(admin.ModelAdmin):
    list_display = ("id", "instrument_configuration", "scraper_type", "created", "source")
    list_filter = ("scraper_type",)
    ordering = ("-created",)
