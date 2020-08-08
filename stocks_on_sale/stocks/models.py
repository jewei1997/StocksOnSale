from django.db import models


class Stock(models.Model):
    ticker = models.CharField(max_length=10, primary_key=True)
    # allowed to be blank/null. If stock has infinite pe ratio, should be float("nan")
    pe_ratio = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"{self.ticker}, PE: {self.pe_ratio}"
