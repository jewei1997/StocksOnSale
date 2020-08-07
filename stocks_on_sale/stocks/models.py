from django.db import models


class Stock(models.Model):
    ticker = models.CharField(max_length=10, primary_key=True)

    def __str__(self):
        return self.ticker
