from django.contrib import admin

from . import models


class InstrumentConfigurationInline(admin.StackedInline):
    model = models.InstrumentConfiguration
    extra = 0


@admin.register(models.Instrument)
class InstrumentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "code", "isin", "bloomberg_code")
    search_fields = ("name", "code", "isin", "bloomberg_code")
