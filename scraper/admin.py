import json

from django.contrib import admin
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import JsonLexer

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


@admin.register(models.ReportType)
class ReportTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "created")
    search_fields = ("id",)
    ordering = ("-created",)


@admin.register(models.ScrapedData)
class ScrapedDataAdmin(admin.ModelAdmin):
    list_display = ("id", "instrument_configuration", "report_type", "created", "source_type")
    list_filter = ("report_type",)
    ordering = ("-created",)
    autocomplete_fields = ("instrument_configuration",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "approved",
                    "approved_at",
                    "instrument_configuration",
                    "report_type",
                    "source_type",
                    "data_prettified",
                    "created",
                ),
            },
        ),
    )
    search_fields = (
        "=id",
        "instrument_configuration__instrument__name",
        "instrument_configuration__instrument__code",
        "instrument_configuration__instrument__isin",
    )

    readonly_fields = (
        "approved_at",
        "created",
        "data_prettified",
    )

    @admin.display(description="Data")
    def data_prettified(self, instance):
        """Function to display pretty version of our data"""

        # Convert the data to sorted, indented JSON
        response = json.dumps(instance.data, sort_keys=True, indent=2)

        # Truncate the data. Alter as needed
        response = response[:5000]

        # Get the Pygments formatter
        formatter = HtmlFormatter(style="colorful")

        # Highlight the data
        response = highlight(response, JsonLexer(), formatter)

        # Get the stylesheet
        style = "<style>" + formatter.get_style_defs() + "</style><br>"

        # Return the output as a plain string (Django will auto-escape)
        return style + response
