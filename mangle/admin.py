from django.contrib import admin

from . import models


class InstrumentConfigurationInline(admin.StackedInline):
    model = models.InstrumentConfiguration
    extra = 0


@admin.register(models.Instrument)
class InstrumentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "code", "isin", "bloomberg_code")
    search_fields = ("name", "code", "isin", "bloomberg_code")
    inlines = [InstrumentConfigurationInline]


@admin.register(models.YieldReport)
class YieldReportAdmin(admin.ModelAdmin):
    list_display = ["id", "instrument", "report_at"]


@admin.register(models.YieldData)
class YieldDataAdmin(admin.ModelAdmin):
    list_display = ["id", "instrument", "yield_interval", "yield_value", "yield_at"]
    raw_id_fields = ["instrument", "report"]
    readonly_fields = ["created"]


@admin.register(models.LastYieldData)
class LastYieldDataAdmin(admin.ModelAdmin):
    list_display = ["id", "instrument", "yield_interval", "yield_at", "yield_value"]
    raw_id_fields = ["instrument"]
    readonly_fields = ["created"]
