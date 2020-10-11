from django.contrib import admin
from .models import TinyURL, TinyURLStats


# Register your models here.
class TinyURLAdmin(admin.ModelAdmin):
    list_display = ("shortcode", "url")


class TinyURLStatsAdmin(admin.ModelAdmin):
    list_display = ("shortcode", "week", "year")
    list_filter = ("year", "week")


admin.site.register(TinyURL, TinyURLAdmin)
admin.site.register(TinyURLStats, TinyURLStatsAdmin)
