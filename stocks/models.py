from django.db import models


class Stock(models.Model):
    ticker = models.CharField(max_length=10, primary_key=True)
    pe_ratio = models.FloatField(blank=True, null=True)
    market_cap = models.IntegerField()

    def __str__(self):
        return f"{self.ticker}, PE: {self.pe_ratio}, MC: {self.market_cap}"
