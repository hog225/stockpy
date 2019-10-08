from django.db import models
from django.forms import ModelForm
from django import forms

# Create your models here.


class Market(models.Model):
    market_name = models.CharField(max_length=25)

    def __str__(self):
        return self.market_name

class TechAnal(models.Model):
    tech_anal_name = models.CharField(max_length=50)

    def __str__(self):
        return self.tech_anal_name

class Stock(models.Model):
    stock_name = models.CharField(max_length=50)
    stock_code = models.CharField(max_length=50)
    f_market = models.ForeignKey(Market, on_delete=models.CASCADE, related_name='stock')

class StockValue(models.Model):
    f_stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='stockvalue', null=True)
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    open = models.FloatField()
    adj_close = models.FloatField()
    volume = models.IntegerField()
    date = models.DateTimeField()
    update_date = models.DateTimeField()


