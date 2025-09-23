from django.contrib import admin

from . import models


@admin.register(models.Instrument)
class InstrumentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "code", "isin", "bloomberg_code")
    search_fields = ("name", "code", "isin", "bloomberg_code", "=id")
    list_filter = ("instrument_type",)
