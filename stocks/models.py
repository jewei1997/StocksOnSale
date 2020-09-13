from django.db import models


class Stock(models.Model):
    ticker = models.CharField(max_length=10, primary_key=True)
    pe_ratio = models.FloatField(blank=True, null=True)
    market_cap = models.BigIntegerField()
    one_week_percentage_change = models.FloatField(blank=True, null=True)
    one_month_percentage_change = models.FloatField(blank=True, null=True)
    one_year_percentage_change = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"{self.ticker}, PE: {self.pe_ratio}, MC: {self.market_cap}, " \
               f"1 Week: {self.one_week_percentage_change}, " \
               f"1 Month: {self.one_month_percentage_change}, " \
               f"1 Year: {self.one_year_percentage_change}"
