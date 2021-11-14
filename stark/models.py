from django.db import models


# Create your models here.
class ExchangeRate(models.Model):
    objects = None
    from_currency_code = models.CharField(null=True, max_length=10)
    from_currency_name = models.CharField(null=True, max_length=60)
    to_currency_code = models.CharField(null=True, max_length=10)
    to_currency_name = models.CharField(null=True, max_length=60)
    exchange_rate = models.FloatField(null=True)
    last_refreshed = models.DateTimeField(null=True)
    time_zone = models.CharField(null=True, max_length=10)
    bid_price = models.FloatField(null=True)

    def __str__(self):
        return "Exchange Rate: {}->{}".format(self.from_currency_code, self.to_currency_code)