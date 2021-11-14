from django.contrib import admin
from .models import ExchangeRate


class ExchangeRateAdmin(admin.ModelAdmin):
    list_display = ('from_currency_code','to_currency_code','exchange_rate',)
    search_fields = ('from_currency_code','to_currency_code')

    class Meta:
        model = ExchangeRate


admin.site.register(ExchangeRate, ExchangeRateAdmin)
